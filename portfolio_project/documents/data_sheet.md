# Datasheet for the Stomata Morphometry Image Dataset

---

## Motivation

The dataset was created to develop and evaluate computer vision methods that automatically measure stomatal anatomical traits (size, density, pore geometry) and estimate maximal stomatal conductance (gsmax) from leaf epidermal micrographs. Manual morphometric analysis is slow and prone to human error. A curated, pixel‐level annotated dataset allows the training of semantic segmentation networks that preserve morphometry, enabling high-throughput phenotyping of crop and tree species.

The dataset was assembled by the Plant Phenotyping and Computer Vision group at the University of Nottingham, United Kingdom. Primary collection, curation and annotation were led by **Jonathon Gibbs** with contributions from Alexandra Burgess, Lorna McAusland and Carlos Robles-Zazueta. Funding was provided by the Biotechnology and Biological Sciences Research Council (grant BB/R004633/1) and the Leverhulme Trust.

---

## Composition

• **Instances**: High-resolution grayscale microscopy images of leaf impressions and their corresponding single-channel semantic masks.

• **Image classes**: Background (discard), guard cells, stomatal pores. Masks encode classes using the values 255, 34/23 and 120/150 depending on species and labelling convention.

• **Datasets**:
  – *Wheat* (monocot): 348 images, 2592 × 1944 px, nail-varnish impressions of flag leaves from eight spring bread wheat cultivars grown under yield-potential glasshouse conditions.
  – *Poplar* (dicot): 114 images, 2048 × 2048 px, balsam poplar impressions originally published by Fetter *et al.* (2019); a carefully re-annotated subset is included here.

• **Annotations**: Every pixel is labelled manually using the Pixel Annotation Tool. No instances are partially labelled.

• **Missing data**: A small minority of raw images were discarded owing to motion blur or poor focus. All retained images have complete masks. There are no empty labels.

• **Confidential data**: None. Images show plant epidermis only and contain no personal or sensitive information.

---

## Collection process

**Acquisition protocol**

1. Leaf impressions were taken using clear nail varnish (wheat) or the method described by Fetter *et al.* (poplar).
2. Dried impressions were mounted on microscope slides and imaged with a Leica DM5000 B light microscope at 40× objective magnification (10 × 40 overall) using transmitted light.
3. Images were saved as 24-bit PNG, then converted to 8-bit single-channel (grayscale).

**Sampling strategy**

Wheat genotypes were selected from the Photosynthesis Respiration Tails (PS Tails) panel to provide diverse canopy architecture. For each plant, both adaxial and abaxial surfaces were sampled at the mid-lamina region. Poplar images were selected to span a range of stomatal densities and impression qualities.

**Time frame**

Wheat images were captured between May and July 2019. Poplar images were downloaded and re-annotated in 2020.

---

## Pre-processing, cleaning and labelling

• **Cropping and padding**: During training, images are divided into overlapping 768 × 768 px tiles. Padding to multiples of 256 px is applied to preserve context at the border.

• **Data augmentation**: Random rotation (±30 °), horizontal/vertical flips (20 % probability), scaling (0.7–1.1), Gaussian blur, unsharp masking, contrast and sharpness adjustments are applied on-the-fly. These augmentations are used only at training time; the saved dataset retains the original pixels.

• **Labelling tool**: Pixel Annotation Tool v1.0. Annotators achieved consensus through iterative review to minimise inter-rater variability.

• **Raw data retention**: All original micrographs are stored alongside the processed dataset in the GitHub repository to support future re-processing.

---

## Uses

Primary use is training and benchmarking semantic segmentation networks that measure stomatal morphometry and estimate gsmax. Additional possible uses include:

• Automatic counting of stomata, guard-cell classification, or species discrimination between monocot and dicot stomatal complexes.

• Transfer learning experiments in botanical or microscopic image domains.

• Educational demonstrations of plant anatomy and computer vision techniques.

**Potential risks**: The dataset is plant-only and poses minimal ethical or legal risk. Nevertheless, users should avoid misinterpreting model performance as indicative of physiological function outside the described species or imaging conditions. Domain shift to other magnifications or illumination settings may generate inaccurate measurements.

**Prohibited uses**: The dataset should not be used to develop biometric systems for human identification or any application unrelated to plant science.

---

## Distribution

The dataset is publicly available via GitHub (https://github.com/DrJonoG) under the MIT licence for code and Creative Commons Attribution 4.0 International (CC BY 4.0) for images and masks. Users must cite Gibbs *et al.* (in preparation) and, for the poplar subset, Fetter *et al.* (2019).

---

## Maintenance

The dataset is maintained by **Jonathon Gibbs** (jonathon.gibbs1@nottingham.ac.uk). Queries, pull requests and issue reports can be submitted through the GitHub repository. Updates will be versioned and documented in the repository's change log.

