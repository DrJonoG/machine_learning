# Model Card

## Model Description

**Input:** Grayscale microscopy images of leaf surfaces (768×768 pixels) containing stomata structures. Images are preprocessed by padding to multiples of 256 pixels and normalised to values between 0 and 1.

**Output:** Multi-class segmentation masks with 3 classes: background (0), guard cells (1), and stomatal pores (2). The model outputs probability maps that are converted to class predictions using argmax.

**Model Architecture:** Attention U-Net with custom attention blocks. The architecture includes:
- Encoder-decoder structure with skip connections
- Attention gates to focus on relevant stomatal features
- Branch convolutional blocks with multiple kernel sizes (1×1, 3×3, 5×5)
- Incremental depth processing for multi-scale feature extraction
- ConvTranspose2d upsampling layers for precise segmentation

## Performance

The model is trained using Lovász-Softmax loss function, which is particularly effective for segmentation tasks with class imbalance. Performance is evaluated using:
- **mIOU (mean Intersection over Union)**: Primary metric for segmentation accuracy
- **Overall pixel accuracy**: Percentage of correctly classified pixels
- **Per-class accuracy**: Individual class performance metrics

Training employs SGD optimiser with learning rate 0.1 and momentum 0.9 over 200 epochs. The model saves checkpoints based on highest mIOU and lowest validation loss. Performance metrics are tracked and saved as CSV files for analysis.

## Limitations

- **Domain specificity**: Model is trained specifically for stomatal segmentation and may not generalise to other plant structures
- **Image quality dependency**: Performance degrades with low-resolution or poorly focused microscopy images
- **Species variation**: Trained primarily on wheat and poplar specimens, may require retraining for other plant species
- **Lighting conditions**: Requires consistent illumination and contrast for optimal performance
- **Computational requirements**: Requires CUDA-enabled GPU for training and inference

## Trade-offs

- **Accuracy vs speed**: Higher resolution inputs (768×768) provide better segmentation accuracy but increase computational cost and inference time
- **Augmentation vs overfitting**: Extensive data augmentation (scaling, rotation, filtering) improves generalisation but increases training time
- **Model complexity vs interpretability**: Attention mechanisms improve performance but reduce model interpretability
- **Memory vs batch size**: Large input images limit batch size (typically 5), affecting training stability
- **Multi-class precision**: Distinguishing between guard cells and pores requires careful threshold tuning, potentially affecting boundary accuracy

## Model Details

- **Parameter count:** Approximately 8.1 million trainable parameters.
- **Framework:** PyTorch 1.11.
- **Input size during training:** 1 × 768 × 768 (channels × height × width).
- **Checkpoint format:** `.pt` file containing model weights and architecture.
- **Training hardware:** Nvidia Titan V (12 GB VRAM), single GPU.
- **Training duration:** 176 minutes for 200 epochs on the wheat dataset.

## Training Data

A total of 462 annotated images: 348 wheat and 114 poplar micrographs. Full dataset details and licensing are provided in `documents/data_sheet.md`.

## Evaluation

After 200 epochs on the wheat validation subset:

Metric | Value
------ | -----
Mean IOU | 0.87
Overall accuracy | 0.95
Guard cell IOU | 0.82
Pore IOU | 0.83

Poplar validation results are comparable with mean IOU 0.85.

## Hyperparameter Optimisation

Small grid search explored learning rates {0.05, 0.1, 0.2}, momentum {0.8, 0.9}, loss {cross-entropy, Lovász-Softmax}. The chosen configuration (lr 0.1, momentum 0.9, Lovász loss) maximised validation IOU while keeping training stable.

## Environmental Impact

Training consumed roughly 0.26 kWh (176 minutes on a 300 W GPU), producing an estimated 0.07 kg CO₂-eq when using the UK national grid average of 0.27 kg CO₂ per kWh. Retraining or hyperparameter sweeps will increase this footprint.

## Intended Use

The model is intended for plant science research, crop phenotyping, and education. It should not be applied to images outside the leaf epidermal microscopy domain without further validation.

## Ethical Considerations

The model analyses plant imagery only. No personal data are involved. Users must ensure responsible use of proprietary plant material and comply with local regulations on genetic resources.

## Citation

If you use this model, please cite:

Gibbs JA, Burgess AJ, McAusland L, Robles-Zazueta CA, Murchie EH (2023). *A deep learning method for fully automatic stomatal morphometry and maximal conductance estimation.*

## Maintenance

Maintainer: Jonathon Gibbs <jonathon.gibbs1@nottingham.ac.uk>. Updates and issue tracking occur via https://github.com/DrJonoG.
