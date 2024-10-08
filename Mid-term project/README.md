# LLM Output Classifier

This project implements a classification model to distinguish between outputs generated by different Large Language Models (LLMs), including GPT-2, GPT-Neo, Falcon, and Facebook OPT. The classifier uses embeddings derived from BERT to classify (xi, xj) sentence pairs into one of these models.

## Dataset

The dataset consists of pairs of text prompts (xi) and completions (xj) generated by various LLMs. These pairs are labeled based on the model that generated the completions.

### Data Files

- `xi_file_path`: File containing prompt texts (xi).
- `xj_file_path`: File containing completion texts (xj) generated by the LLMs.
- The `classifier.py` script loads these files to create labeled datasets.

## Features

- **BERT-based Embedding Extraction**: The script uses a pre-trained BERT model to generate embeddings for the (xi, xj) sentence pairs.
- **Custom Neural Network Classifier**: A fully connected neural network is used to classify the embeddings into one of the four LLMs.
- **Model Training with Early Stopping**: Implements early stopping to avoid overfitting during training.
- **Evaluation**: Provides accuracy and a classification report to assess the model's performance.

## Requirements

The following libraries are required to run the script:

- Python 3.7+
- pandas
- transformers (Hugging Face)
- torch (PyTorch)
- scikit-learn

You can install the dependencies using pip:

```bash
pip install pandas transformers torch scikit-learn
```
## Usage

### 1. Prepare the Dataset:

- Ensure that the `xi` and `xj` text files are available. These files should contain paired sentences from different LLMs.
- Each line in the `xi` file should correspond to a prompt, and the respective line in the `xj` file should contain the completion.

### 2. Run the Classifier:

- Load the data, generate embeddings using BERT, and train the classifier by running the script:

```bash
python classifier.py
```
### 3. Training and Evaluation:

- The script prints the training loss and validation accuracy for each epoch. After training, the best model is saved as `best_model.pt`, and the final test accuracy and classification report will be displayed.

## Key Functions

- **`load_xi_xj_pairs(xi_file_path, xj_file_path, label)`**: Loads pairs of sentences (`xi` and `xj`) from the provided file paths and returns a labeled dataset.

- **`get_embeddings(xi, xj)`**: Generates BERT embeddings for the input sentence pairs.

- **`train_model()`**: Trains the neural network using the generated embeddings.

- **`evaluate_model()`**: Evaluates the trained model on the test set and prints a classification report.

## Output

- **Test Accuracy and Report**: The model outputs the accuracy of classification among GPT-2, GPT-Neo, Falcon, and Facebook OPT.

- **Saved Model**: The best model is saved as `best_model.pt` and can be reused for inference on new data.
