import os
import json
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Set your Hugging Face token
DistilBERTtoken = "your_huggingface_token_here"

# Load the tokenizer and model
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name, token=DistilBERTtoken)
model = DistilBertForSequenceClassification.from_pretrained(model_name, token=DistilBERTtoken, num_labels=4)

# Load and preprocess dataset
def load_and_preprocess_data(json_file):
    label_mapping = {"PROCESS": 0, "TOOL_FAILURE": 1, "COLLISION": 2, "OPERATIONAL_ERROR": 3} # Define label mapping
    with open(json_file, 'r') as f:
        data = json.load(f)
    prompts = [item['prompt'] for item in data]
    labels = [label_mapping[item['label']] for item in data]  # Map labels to numerical values
    encodings = tokenizer(prompts, padding=True, truncation=True, max_length=200)
    labels_tensor = torch.tensor(labels, dtype=torch.long) # Ensure labels are tensors
    dataset = Dataset.from_dict({
        'input_ids': encodings['input_ids'],
        'attention_mask': encodings['attention_mask'],
        'labels': labels_tensor
        })
    return dataset

# Create your synthetic data file 'synthetic_data.json'
synthetic_data = [
    {"prompt": "Process2 Failure", "label": "PROCESS"},
    {"prompt": "Process1 Failure", "label": "PROCESS"},
    {"prompt": "Crane's vacuum gripper tool failure", "label": "TOOL_FAILURE"},
    {"prompt": "Colloison during placing part on running process", "label": "COLLISION"},
    {"prompt": "Miscommunication, Overloading, and Crane Path Obstruction", "label": "OPERATIONAL_ERROR"},
]


with open('synthetic_data.json', 'w') as f:
    json.dump(synthetic_data, f)

train_dataset = load_and_preprocess_data('synthetic_data.json')
eval_dataset = load_and_preprocess_data('synthetic_data.json')

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer
)

# Train the model
trainer.train()


# Assuming your model and tokenizer are already defined and trained
model_name = "./trained_model"

# Save the trained model
model.save_pretrained(model_name)

# Save the tokenizer
tokenizer.save_pretrained(model_name)

