import torch
import time
import numpy as np
import lovasz_losses as L

from utils import progress, saveloss, open_image, save_prediction
from torch.utils.data import Dataset, DataLoader
from datasets import CustomDataset
from model import Model
from torch import nn, save
from torchsummary import summary
from pathlib import Path
from PIL import Image
import torch.nn.functional as F
from matplotlib import pyplot as plt
from IOUEval import iouEval #importing iouEval class
from sklearn.metrics import jaccard_score as jsc
from torch.optim.lr_scheduler import StepLR
from torch.cuda.amp import autocast, GradScaler  # mixed precision (Module_019)

class Trainer(object):
    def __init__(self, in_channels=None, out_channels=None, labels=None, model_dir=None, model_path=None, network=None, augmentation=None):
        self.model_path = model_dir

        self.device_model = torch.device("cuda:0")
        self.device_data = torch.device("cuda:0")

        if model_path == None:
            self.train_dl = None
            self.valid_dl = None
            # Network type
            self.model =  Model.AttU_Net(in_channels, out_channels)

            self.model = torch.nn.DataParallel(self.model)
            self.model.to(f'cuda:{self.model.device_ids[0]}')
        else:
            self.model = torch.load(model_path)
            self.model.cuda()
            self.model.eval()

        self.classes = out_channels
        self.labels = (-np.sort(-labels)).astype(int)
        self.augmentations = augmentation
        #self.model = nn.DataParallel(self.model, device_ids=[0])

    def DataLoader(self, batch_size, path):
        base_path = Path(path)
        train_ds = CustomDataset.CustomDataset(self.augmentations, base_path/'train_samples', base_path/'train_mask', self.labels)
        valid_ds = CustomDataset.CustomDataset(self.augmentations, base_path/'valid_samples', base_path/'valid_mask', self.labels)
        #train_ds, valid_ds = torch.utils.data.random_split(data, [int(len(data)*0.8), len(data) - int(len(data)*0.8)])

        self.train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=4)
        self.valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=True, num_workers=4)

    def predict(self, directory_in, directory_out, annotation):
        start = time.time()

        dir = Path(directory_in)
        files = [f for f in dir.iterdir() if not f.is_dir()]

        file_count = len(files)
        step = 0
        for file in files:
            step += 1

            img_o = torch.tensor(open_image(file))
            img = img_o.unsqueeze(0)
            img = img.to(device='cuda', dtype=torch.float32)

            #summary(model, input_size=(4,384,384))
            with torch.no_grad():
                pred = self.model(img.cuda())

            pred = torch.functional.F.softmax(pred[0], 0)
            pred = (pred.argmax(0).cpu()).numpy()

            save_prediction(pred, file, directory_out, annotation, self.labels)

            time_elapsed = time.time() - start
            start_string = 'Image %s/%s:' % (step, file_count)
            end_string = 'Predicting: %s  Runtime %.0fm %.0fs' % \
                (Path(file).name, time_elapsed // 60, time_elapsed % 60)
            progress(step, file_count, prefix = start_string, suffix = end_string, length = 30)

    def acc_metric(self, predb, yb):
        return (predb.argmax(dim=1) == yb.cuda()).float().mean()

    def train(self, path, batch_size, epochs):
        # Load data
        self.DataLoader(batch_size, path)

        # Initialise optimiser and learning-rate scheduler (Module_019: Hyperparameters)
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-4)
        scheduler = StepLR(optimizer, step_size=30, gamma=0.1)

        # Initialise GradScaler for mixed precision
        scaler = GradScaler()

        iouEvalTrain = iouEval(self.classes)
        iouEvalTest = iouEval(self.classes)

        train_loss, valid_loss = [], []
        iou_acc_train, iou_acc_valid = [], []
        iou_valid, iou_train = [], []
        per_class_acc_valid = []
        precision_list, recall_list, f1_list = []

        start = time.time()
        valid_loss_min = float("inf")
        iou_loss_min = -float("inf")

        # Early stopping parameters (see Module_019 – Early Stopping)
        patience = 10
        epochs_no_improve = 0

        print(summary(self.model, (1, 768,768)))

        # Begin training
        for epoch in range(epochs):
            for phase in ['train', 'valid']:
                # Reset IoU evaluator at the start of each phase
                if phase == 'train':
                    iouEvalTrain.reset()
                else:
                    iouEvalTest.reset()

                if phase == 'train':
                    self.model.train(True)  # Set trainind mode = true
                    dataloader = self.train_dl
                else:
                    self.model.train(False)  # Set model to evaluate mode
                    dataloader = self.valid_dl

                # Declare and initialise variables as 0
                running_loss = 0.0
                running_acc = 0.0
                step = 0

                # iterate over data
                for x, y in dataloader:
                    x, y = x.cuda(), y.cuda()
                    step += 1
                    # forward pass
                    if phase == 'train':
                        with autocast():
                            outputs = self.model(x)
                            outputs = F.softmax(outputs, dim=1)
                            loss = L.lovasz_softmax(outputs,  y)

                        optimizer.zero_grad()
                        scaler.scale(loss).backward()
                        scaler.step(optimizer)
                        scaler.update()

                        iouEvalTrain.addBatch(outputs.max(1)[1].unsqueeze(1).data, y.data)
                        overall_acc, per_class_acc, per_class_iu, mIOU = iouEvalTrain.getMetric()

                        running_loss += loss.item()
                        running_acc += overall_acc
                    else:
                        with torch.no_grad(), autocast():
                            outputs = self.model(x)
                            outputs = F.softmax(outputs, dim=1)
                            loss = L.lovasz_softmax(outputs, y)

                            iouEvalTest.addBatch(outputs.max(1)[1].unsqueeze(1).data, y.data)
                            overall_acc, per_class_acc, per_class_iu, mIOU = iouEvalTest.getMetric()

                            running_loss += loss.item()
                            running_acc += overall_acc

                            # Compute confusion-matrix-derived metrics (Module_006 – Performance Evaluation)
                            # Convert tensors to CPU numpy for sklearn metrics
                            preds_flat = outputs.max(1)[1].view(-1).cpu().numpy()
                            labels_flat = y.view(-1).cpu().numpy()
                            # Ignore pixels where label == 255 (void) if present
                            mask_valid = labels_flat != 255
                            preds_flat = preds_flat[mask_valid]
                            labels_flat = labels_flat[mask_valid]

                            if len(np.unique(labels_flat)) > 1:  # avoid undefined metrics
                                from sklearn.metrics import precision_score, recall_score, f1_score
                                precision_list.append(precision_score(labels_flat, preds_flat, average='macro', zero_division=0))
                                recall_list.append(recall_score(labels_flat, preds_flat, average='macro', zero_division=0))
                                f1_list.append(f1_score(labels_flat, preds_flat, average='macro', zero_division=0))

                    time_elapsed = time.time() - start
                    current_lr = optimizer.param_groups[0]['lr']
                    start_string = 'Epoc (%s) %s/%s:' % (phase, epoch + 1, epochs)
                    end_string = 'Step: %s LR: %.6f Loss: %.3f  Running Loss: %.3f  Running Acc: %.3f mIOU: %.3f Runtime %.0fm %.0fs' \
                                % (step, current_lr, loss, running_loss / step , running_acc / step, mIOU, time_elapsed // 60, time_elapsed % 60)
                    progress(step, len(dataloader), prefix = start_string, suffix = end_string, length = 20)

                epoch_loss = running_loss / len(dataloader.dataset)
                epoch_acc = running_acc / len(dataloader.dataset)

                if phase=='train':
                    train_loss.append(epoch_loss)
                    overall_acc, per_class_acc, per_class_iu, mIOU = iouEvalTrain.getMetric()
                    iou_acc_train.append(overall_acc)
                    iou_train.append(mIOU)
                else:
                    with torch.no_grad():
                        valid_loss.append(epoch_loss)
                        overall_acc, per_class_acc, per_class_iu, mIOU = iouEvalTest.getMetric()
                        iou_acc_valid.append(overall_acc)
                        per_class_acc_valid.append(per_class_iu)
                        iou_valid.append(mIOU)

                        if mIOU >= iou_loss_min:
                            print('==> IOU increased ({:.4f} --> {:.4f}).  Saving model ...'.format(
                            iou_loss_min,\
                            mIOU))
                            torch.save(self.model, self.model_path + 'highest_iou_wheat.pt')
                            iou_loss_min = mIOU

                        if epoch_loss <= valid_loss_min:
                            print('==> Loss decreased ({:.4f} --> {:.4f}).  Saving model ...'.format(
                            valid_loss_min,\
                            epoch_loss))
                            torch.save(self.model, self.model_path + 'lowest_loss_wheat.pt')
                            valid_loss_min = epoch_loss
                            epochs_no_improve = 0  # reset counter if validation improves
                        else:
                            epochs_no_improve += 1

            # Step the LR scheduler after each epoch (Module_005 – Bias-Variance)
            scheduler.step()

            # Early stopping check
            if epochs_no_improve >= patience:
                print(f"==> Early stopping triggered after {patience} epochs without improvement.")
                break

        time_elapsed = time.time() - start
        print('==> Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

        np.savetxt(self.model_path + '0.train_loss.csv', train_loss, delimiter=",")
        np.savetxt(self.model_path + '0.valid_loss.csv', valid_loss, delimiter=",")
        np.savetxt(self.model_path + '0.iou_train.csv', iou_train, delimiter=",")
        np.savetxt(self.model_path + '0.iou_valid.csv', iou_valid, delimiter=",")
        np.savetxt(self.model_path + '0.iou_acc_train.csv', iou_acc_train, delimiter=",")
        np.savetxt(self.model_path + '0.iou_acc_valid.csv', iou_acc_valid, delimiter=",")
        np.savetxt(self.model_path + '0.per_class_acc_valid.csv', per_class_acc_valid, delimiter=",")

        # Save additional confusion-matrix metrics
        if len(precision_list):
            np.savetxt(self.model_path + '0.precision.csv', np.array(precision_list), delimiter=",")
            np.savetxt(self.model_path + '0.recall.csv', np.array(recall_list), delimiter=",")
            np.savetxt(self.model_path + '0.f1.csv', np.array(f1_list), delimiter=",")

        torch.save(self.model.state_dict(), self.model_path + 'final.pth')
        torch.save(self.model, self.model_path + 'final.pt')
        #saveloss(path_string, train_loss, valid_loss)
