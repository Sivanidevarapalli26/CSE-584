# -*- coding: utf-8 -*-
"""Falcon-7b_LLM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YIDKQqbEq2LUGPS0-PNCdz1ElgBmOXkz
"""

#LLM: falcon-7b
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load Falcon-7B model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b")
tokenizer.pad_token = tokenizer.eos_token  # Set padding to left and assign the eos_token as the pad_token
tokenizer.padding_side = 'left'

model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b", torch_dtype=torch.bfloat16, device_map="auto")

# Input and output files
input_file = "/content/truncated_sentences.txt"
output_file = "/content/falcon_sentences.txt"

# Batch size and max length of sentence needed
BATCH_SIZE = 32
MAX_LENGTH = 40


def read_sentences(input_file):
    with open(input_file, 'r') as f:
        sentences = [line.strip() for line in f if line.strip()]
    return sentences

# Function to generate completions for a batch of sentences
def generate_completions(sentences, max_length=MAX_LENGTH):
    # Tokenize input with left padding
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    input_ids = inputs['input_ids'].to(model.device)
    attention_mask = inputs['attention_mask'].to(model.device)

    # Generate completions
    with torch.no_grad():
        outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length, do_sample=True, top_p=0.9)
    completions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return completions

def write_completions(completions, output_file):
    with open(output_file, 'w') as f:
        for sentence in completions:
            f.write(sentence + '\n')

def process_file(input_file, output_file, batch_size=BATCH_SIZE):
    sentences = read_sentences(input_file)
    all_completions = []
    for i in range(0, len(sentences), batch_size):
        batch_sentences = sentences[i:i + batch_size]
        completions = generate_completions(batch_sentences)
        all_completions.extend(completions)

    # Write all completed sentences to output file
    write_completions(all_completions, output_file)

# Run the process
if __name__ == "__main__":
    process_file(input_file, output_file)
    print(f"Completed sentences saved to {output_file}")

# Function to find the number of lines (complete sentences) in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()
        # Remove empty lines and count the number of non-empty lines
        non_empty_lines = [line for line in lines if line.strip()]  # Strip removes spaces or newline characters
    return len(non_empty_lines)

# Example usage
file_path = "/content/finalfalcon_sentences.txt"
num_lines = count_lines_in_file(file_path)
print(f"The file contains {num_lines} complete sentences.")

# Function to remove lines with only whitespaces from a file
def remove_whitespace_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove empty lines or lines containing only whitespace, and strip extra spaces from each line
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    return non_empty_lines

# Function to keep lines in complete_sentences.txt that start with sentences from truncated_sentences.txt
def keep_matching_lines(complete_sentences_file, truncated_sentences_file, output_file):
    # Get non-empty lines from both files
    complete_sentences = remove_whitespace_lines(complete_sentences_file)
    truncated_sentences = remove_whitespace_lines(truncated_sentences_file)

    matching_sentences = []

    # Find lines in complete_sentences that start with any sentence from truncated_sentences
    for complete_sentence in complete_sentences:
        if any(complete_sentence.startswith(truncated_sentence) for truncated_sentence in truncated_sentences):
            matching_sentences.append(complete_sentence)

    # Write the matching sentences to an output file
    with open(output_file, 'w') as file:
        for sentence in matching_sentences:
            file.write(sentence + '\n')

    return len(matching_sentences)  # Return the count of matching sentences

# Example usage
complete_sentences_file = "/content/falcon_sentences.txt"
truncated_sentences_file = "/content/truncated_sentences.txt"
output_file = "finalfalcon_sentences.txt"

# Keep matching sentences and write them to the output file
matching_line_count = keep_matching_lines(complete_sentences_file, truncated_sentences_file, output_file)

print(f"Number of matching lines written to {output_file}: {matching_line_count}")