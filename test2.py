import torch
from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_id = "meta-llama/Llama-3.2-3B-Instruct"
logger.info(f"Loading model: {model_id}")

# Load pipeline
try:
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto"  # Ensure the model is loaded onto available hardware
    )
    logger.info("Pipeline loaded successfully.")
except Exception as e:
    logger.error(f"Error loading pipeline: {e}")
    pipe = None  # Ensure pipe is defined even if loading fails

# Simple prompt to test text generation
prompt = "Hello"

if pipe is not None:
    try:
        logger.info("Generating text...")
        outputs = pipe(
            prompt,
            max_new_tokens=20,  # Reduced for quicker results
            temperature=0.7,    # Adjusted for better creativity
            top_k=50,
            top_p=0.9
        )
        generated_text = outputs[0]["generated_text"]
        logger.info(f"Generated text: {generated_text}")
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        generated_text = "Error generating text."
else:
    generated_text = "Pipeline failed to load."

print("Generated response:", generated_text)
