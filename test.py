import os
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure your environment variable is set
huggingface_token = os.getenv("HUGGINGFACE_HUB_TOKEN_3.2-3B-instruct", "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")

model_name = "meta-llama/Llama-3.2-3B-Instruct"
logger.info(f"Loading model: {model_name}")

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=huggingface_token)
    logger.info("Tokenizer loaded successfully.")
    model = AutoModelForCausalLM.from_pretrained(model_name, token=huggingface_token)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    exit(1)  # Exit if the model loading fails

# Set pad_token_id if not already set
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=200,
        pad_token_id=tokenizer.pad_token_id,
        temperature=0.7,  # Adjust temperature
        top_k=50,         # Adjust top_k sampling
        top_p=0.9         # Adjust top_p nucleus sampling
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

prompt = "Provide detailed mitigation steps for the hazard: Robot collision with operator in an industrial environment."
try:
    response = generate_text(prompt)
    logger.info(f"Generated response: {response}")
except Exception as e:
    logger.error(f"Error generating text: {e}")
    response = "Error generating mitigation steps."

print("Generated response:", response)
