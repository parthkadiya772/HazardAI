from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

distilbert_app = Flask(__name__)
CORS(distilbert_app)  # Enable CORS

# Load the tokenizer and model
model_name = "./trained_model"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Function to classify new text
def classify_text(prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        #print(f"Predicted class: {predicted_class}")  # Debugging: Print predicted class
        return predicted_class
    except Exception as e:
        print(f"Error in classify_text: {e}")
        return -1  # Return an invalid class if there's an error

@distilbert_app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data['prompt']
        predicted_class = classify_text(prompt)
        
        if predicted_class == -1:
            raise ValueError("Error during classification")

        mitigations = {
            1: "Crane’s vacuum gripper tool failure \n   -> Risk to Operators:\n       - High risk of part falling and potentially causing injury to operator.\n       - Tool failure leading to operational hazards.\n       - Robot collision with operator or other robots.\n       - Part placing to unspecified place which can cause injury to operator.\n   Mitigations:\n   Ensure regular maintenance of the gripper tool, use fail-safe systems to prevent part drops, and install sensors to detect malfunctions. Implement safety barriers, restricted zones, and operator training to minimize risks of collisions and injuries.",
            2: "Provide proper training and safety equipment",
            0: "Process failure \n   -> Risk to Operators:\n       - High risk of fire in the industry.\n       - Low risk of law quality production or immediate process stop.\n       - High risk of electric shock to Operator which could be a serious hazard.\n   Mitigations:\n   Implement robust fire prevention systems, including fire alarms and extinguishers, and conduct regular inspections of electrical systems to prevent shocks. Ensure proper grounding, insulation, and emergency power shut-offs. Train operators on emergency response protocols and maintain equipment to minimize process failures and ensure consistent production quality.",
            4: "Install fire alarms and have fire extinguishers accessible",
            3: "Miscommunication, Overloading, and Crane Path Obstruction \n   -> Risk to Operators:\n       - Miscommunication between crane sensors and packaging sensors could lead to improper part placement or timing issues.\n       - Transferring parts that exceed the crane's load capacity may cause equipment failure.\n       - Parts in the crane's designated path may lead to delays, collisions, or accidents.\n   Mitigations:\n   Mitigate operational hazards by ensuring clear communications between sensors and frequent testing of sensors, using load sensors, maintaining clear pathways, and employing real-time monitoring to coordinate crane movements and prevent delays."
        }
        
        mitigation = mitigations.get(predicted_class, "Mitigation step not defined for this hazard")
        return jsonify({'response': mitigation})
    except Exception as e:
        print(f"Error in generate endpoint: {e}")
        return jsonify({'response': 'Error generating mitigation.'})

if __name__ == '__main__':
    distilbert_app.run(host='0.0.0.0', port=5000)
