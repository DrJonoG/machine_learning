# StomataMorph

Automated extraction of stomatal morphometry and estimation of maximal stomatal conductance (gsmax) from leaf epidermal micrographs using deep learning.

## Non-technical overview

Plants breathe through tiny pores called stomata. Their size and number influence how much water a plant loses and how much carbon dioxide it can absorb. Traditionally scientists measure these features by hand, a slow and error-prone task. StomataMorph uses a neural network to find every stoma in a microscope image, measure its dimensions automatically and calculate a physiological trait called gsmax. The tool turns hours of manual work into seconds of computation, helping plant biologists study large populations and speed up crop research.

## Data

• 462 grayscale micrographs (348 wheat, 114 poplar) with pixel-level masks.  
• Captured at 40× magnification; resolutions 2592×1944 or 2048×2048.  
• Annotations contain three classes: background, guard cells, pore.  
• Full details are in `documents/data_sheet.md`.

## Model

An Attention U-Net with inception-style multi-scale branches.

Key features:

- Input tiles 768×768, single channel.
- Encoder-decoder with attention gates for salient feature emphasis.
- Lovász-Softmax loss to optimise mean Intersection over Union (mIOU).
- Implemented in PyTorch (`model/Model.py`).

## Training and hyperparameters

Parameter | Value
--------- | -----
Optimiser | SGD, lr 0.1, momentum 0.9
Batch size | 5 (GPU memory limited)
Epochs | 200
Loss | Lovász-Softmax
Augmentation | Random crop, rotation ±30°, flips, blur/contrast/sharpness

Hyperparameter values were selected via small grid search (see `documents/model_card.md`). Early stopping on validation mIOU prevents over-fitting.

## Results

Validation (wheat subset):

Metric | Value
------ | -----
mIOU | 0.87
Overall pixel accuracy | 0.95
Guard cell IOU | 0.82
Pore IOU | 0.83

The automated gsmax estimates differ on average by 3.8 % (wheat) and 1.9 % (poplar) from expert manual measurements

## Quick start

```bash
# create and activate environment, then
python main.py -c config.ini -o train   # train from scratch
python main.py -c config.ini -o predict # run inference on new images
```

Predictions are saved in `predict/out/` as colour masks and blended overlays.

## Folder structure

```
portfolio_project/
├── datasets/        # data loaders and augmentations
├── documents/       # paper, datasheet, model card
├── model/           # neural network architecture
├── morphometry/     # gsmax and density calculations
├── predict/         # example images and outputs
```

## Requirements

- Python 3.9
- PyTorch ≥ 1.11 with CUDA
- NumPy, SciPy, scikit-image, TorchSummary, scikit-learn, Pillow, Matplotlib

Exact versions are listed in `requirements.txt` (create one if needed).

## Citation

If you use this code or data, please cite:

```
Gibbs JA, Burgess AJ, McAusland L, Robles-Zazueta CA, Murchie EH. A deep learning method for fully automatic stomatal morphometry and maximal conductance estimation. 2023.
```

## Contact

Maintainer: Jonathon Gibbs  
Email: jonathon.gibbs1@nottingham.ac.uk  
GitHub: https://github.com/DrJonoG

