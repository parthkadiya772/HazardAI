import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)
CORS(app)  # Enable CORS

# Ensure your environment variable is set
HUGGINGFACE_HUB_TOKEN = "your_huggingface_token_here"

model_name = "meta-llama/Llama-3.2-1B" # Replace with your model name
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_HUB_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HUGGINGFACE_HUB_TOKEN)

def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100, num_beams=2, top_k=50, temperature=0.7, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
       
    if not prompt:
        app.logger.error("No prompt provided")
        return jsonify({"error": "Prompt is required"}), 400
    try:
        app.logger.info(f"Received prompt: {prompt}")
        response = generate_text(prompt)
        app.logger.info(f"Generated response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error generating text: {str(e)}")
        app.logger.debug(f"Exception details:", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
