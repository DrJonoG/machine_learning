# Machine Learning Course Notes

This repository contains comprehensive notes and concepts from the Machine Learning course at Imperial College London. The course covers fundamental topics in machine learning, providing both theoretical foundations and practical applications.

## File Overview

### Module_002 - Introduction.ipynb
- Introduces the basic concepts of machine learning
- Covers supervised vs unsupervised learning
- Explains key terminology and the machine learning workflow

### Module_003 - Probability.ipynb
- Focuses on probability theory fundamentals
- Covers probability distributions, Bayes' theorem, and conditional probability
- Explains how probability relates to machine learning models

### Module_004 - Statistics.ipynb
- Covers statistical concepts essential for machine learning
- Includes hypothesis testing, confidence intervals, and statistical significance
- Explains descriptive and inferential statistics

### Module_005 - Bias-Variance.ipynb
- Explores the bias-variance tradeoff in machine learning
- Discusses model complexity and generalisation
- Covers techniques to balance bias and variance

### Module_006 - Performance Evaluation.ipynb
- Focuses on evaluating machine learning models
- Covers metrics like accuracy, precision, recall, and F1-score
- Explains confusion matrices and ROC curves

### Module_007 - Cross Validation.ipynb
- Explains cross-validation techniques for model evaluation
- Covers k-fold cross-validation and stratified sampling
- Discusses oversampling techniques for imbalanced datasets

### Module_008 - KNN.ipynb
- Explains the k-Nearest Neighbors algorithm and its implementation
- Covers distance metrics and neighbor selection strategies
- Discusses parameter tuning and the effect of k on model performance

### Module_009 - Decision Trees.ipynb
- Introduces decision tree algorithms and their construction
- Explains splitting criteria and tree growth mechanisms
- Covers pruning techniques and handling categorical variables

### Module_010 - Tree Ensembles.ipynb
- Explores advanced tree-based methods including Random Forests and AdaBoost
- Covers bootstrapping and feature importance evaluation techniques
- Discusses model interpretability and the bias-variance tradeoff in ensembles

### Module_011 - Naive Bayes.ipynb
- Explains the Naive Bayes classification algorithm
- Covers probability-based classification and the independence assumption
- Discusses applications and limitations of Naive Bayes

### Module_012 - Bayesian Optimisation.ipynb
- Introduces Bayesian optimisation techniques for hyperparameter tuning
- Covers acquisition functions and surrogate models
- Explains the exploration-exploitation tradeoff

### Module_013 - Logistic Regression.ipynb
- Covers logistic regression for binary classification
- Explains maximum likelihood estimation and model training
- Discusses regularisation and model interpretation

### Module_014 - SVM.ipynb
- Explains Support Vector Machine algorithms and their mathematical foundations
- Covers kernel tricks and margin optimisation techniques 
- Discusses hyperparameter tuning and multi-class SVM approaches

### Module_015 - Clustering.ipynb
- Introduces unsupervised learning through clustering algorithms
- Covers k-means, hierarchical clustering, and density-based methods
- Explains cluster evaluation metrics and determining optimal cluster numbers

### Module_016 - PCA.ipynb
- Explains Principal Component Analysis for dimensionality reduction
- Covers eigenvalue decomposition and variance explained ratios
- Discusses feature transformation and data visualisation techniques

### Module_017 - Intro To DL.ipynb
- Introduces neural networks and their historical development in deep learning
- Explains the five key building blocks of neural networks including backpropagation and activation functions
- Covers practical aspects like hyperparameter tuning and regularization techniques

### Module_018 - Neural Networks.ipynb
- Details the architecture and components of neural networks, including layers, weights, biases, and activation functions
- Explains function approximation, forward and backward passes, and the use of gradient descent and backpropagation for training
- Discusses practical implementation, types of gradient descent, and when deep learning is a suitable solution

### Module_019 - Hyperparameters.ipynb
- Explores hyperparameter optimization and its crucial role in deep learning model performance
- Covers key hyperparameters including learning rate, batch size, epochs, optimizer types, dropout rates, and weight initialization
- Demonstrates practical implementation differences between NumPy and PyTorch neural networks

### Module_020 - Transparency and Interpretability.ipynb
- Explores transparency and interpretability in machine learning, focusing on the risks of bias in data and models
- Covers real-world consequences of opaque models, such as discrimination and ethical issues
- Introduces tools like Datasheets for Datasets and Model Cards to document and benchmark models
- Discusses methods to detect and mitigate bias, and the importance of regulatory compliance (e.g., UK GDPR)
- Compares Explainable AI (post hoc explanations) and Interpretable AI (inherently transparent models), highlighting trade-offs between complexity and human understanding

### Module_021 - CNNs.ipynb
- Explains convolutional neural networks (CNNs) and their applications in computer vision, NLP and financial time series
- Covers key CNN components including convolutional filters, activation functions, feature maps and pooling layers
- Provides mathematical formulas for calculating output dimensions, parameters and receptive fields
- Discusses important hyperparameters like padding and stride, and how they affect network architecture
- Explores common CNN architectures and the principles of local connectivity and parameter sharing

### Module_022 - Bias for CNN.ipynb
- Explores the biological basis for convolutional neural networks and their connection to visual neuron responses
- Dissects the LeNet-5 architecture and explains how each filter processes computer images
- Covers the three main CNN building blocks: convolutional layers, pooling layers, and fully connected layers
- Provides mathematical formulations for computing output dimensions using filter size, stride, and padding parameters
- Discusses CNN hyperparameter optimization and practical implementation using PyTorch for computer vision systems

### Module_023 - Reinforcement Learning.ipynb
- Introduces reinforcement learning as a sub-area of machine learning where agents learn from trial and error through environmental interaction
- Covers key RL components including actions, expected rewards, and the critical exploration vs exploitation trade-off
- Explains the Multi-Armed Bandit (MAB) problem with real-world applications in A/B testing, drug treatments, and network routing
- Details Markov Decision Processes (MDPs) including states, actions, rewards, episodes, and policy optimization
- Compares model-free approaches (Q-Learning, SARSA, Policy Gradient methods) with model-based approaches (value iteration, policy iteration)
- Demonstrates practical concepts through Markov chains modeling student behavior with transition matrices and state diagrams
- Provides comprehensive coverage of the Bellman equation, discount factors, and value iteration algorithms for optimal policy derivation
- Explains Q-Learning as a model-free algorithm for learning optimal policies without environment models
- Introduces Temporal Difference (TD) learning, combining Monte Carlo methods and dynamic programming for online learning

### Module_024 - Hyperparameters.ipynb
- Advanced exploration of hyperparameter tuning challenges and methodologies in machine learning and deep learning
- Defines critical challenges in hyperparameter optimization including non-stationarity and heteroscedasticity concepts
- Covers comprehensive methods for hyperparameter tuning: handcrafted search, grid search, random search, and Bayesian optimization
- Explores state-of-the-art techniques including batch (parallel) Bayesian optimization for large-scale distributed systems
- Details advanced batch optimization strategies: Constant Liar Method, Local Penalisation, and Thompson Sampling for parallel evaluation
- Discusses modern approaches including multi-fidelity optimization, Hyperband/BOHB, meta-learning, and Neural Architecture Search (NAS)
- Emphasizes the critical impact of hyperparameter selection on model performance and learning efficiency
- Addresses computational efficiency challenges and resource allocation strategies in hyperparameter optimization

### Summary.ipynb
- Provides a comprehensive summary of all course modules
- Includes key concepts, formulas, and practical applications
- Serves as a quick reference guide for the entire course

## Usage
These Jupyter notebooks can be used as study materials, reference guides, or starting points for machine learning projects. Each notebook contains detailed explanations, examples, and important concepts from the course.

## License
These materials are shared with permission from Imperial College London. Please use them responsibly and in accordance with the course's academic integrity policies.
