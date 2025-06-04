# HazardAI

HazardAI is an AI-powered application designed for hazard detection and safety text generation. The project contains both a TypeScript-based frontend (React) and a Python backend for model training and inference.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Structure](#structure)
- [Setup & Installation](#setup--installation)
- [Backend: Python AI](#backend-python-ai)
- [Frontend: React/TypeScript](#frontend-reacttypescript)
- [Training & Testing](#training--testing)
- [Usage](#usage)
- [Results & Models](#results--models)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

HazardAI leverages state-of-the-art machine learning, natural language processing (NLP) to identify and classify hazards; and large language models (LLM) to generate safety text. The application supports:
- Traning/Finetuning large language models (LLM) with your own dataset
- Running inference via a web or API interface
- Visualization and analysis of results

---

## Structure

```
.
├── README.md
├── app.py                    # Python backend server (API)
├── dataset-creation.py       # Script for creating datasets
├── distilbert_app.py         # Python app using DistilBERT for NLP tasks
├── package.json, tsconfig.json, etc. # Frontend configuration
├── public/                   # Frontend static assets
├── results/                  # Output and results from model runs
├── src/                      # Frontend app (React, TypeScript)
├── synthetic_data.json       # Example/synthetic data
├── test.py, test2.py         # Python test scripts
├── training_script.py        # Script for model training
├── trained_model/            # Saved model files
```
*More files may be present. [See the full file list.](https://github.com/parthkadiya772/HazardAI/tree/main)*

---

## Setup & Installation

### Prerequisites

- **Backend:** Python 3.8+, pip, (recommended: venv or conda)
- **Frontend:** Node.js 16+, npm

### Backend Setup

```bash
# Create and activate a virtualenv (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies (example, adjust as needed)
pip install -r requirements.txt
```

### Frontend Setup

```bash
npm install
```

---

## Backend: Python AI

- **app.py**: Main API server (Flask, FastAPI, or similar)
- **distilbert_app.py**: Uses HuggingFace DistilBERT for NLP-based hazard classification
- **training_script.py**: Train models on your own data
- **dataset-creation.py**: Prepare and preprocess datasets

---

## Frontend: React/TypeScript

- **src/**: Main application source code (TypeScript, React)
- **public/**: Static files and HTML
- **package.json**: Project dependencies and scripts
- **tsconfig.json**: TypeScript config

#### Running the Frontend

```bash
npm start
```
App runs on [http://localhost:3000](http://localhost:3000).

---

## Training & Testing

- **training_script.py**: Train models (edit to point to your dataset)
- **test.py**, **test2.py**: Test scripts for validation and evaluation

---

## Usage

1. **Start the backend:**  
   ```bash
   python app.py
   ```
   or
   ```bash
   python distilbert_app.py
   ```

2. **Start the frontend:**  
   ```bash
   npm start
   ```

3. **Access the web interface:**  
   Go to [http://localhost:3000](http://localhost:3000)

---

## Results & Models

- **results/**: Contains output, logs, or exported data
- **trained_model/**: Stores trained model weights and checkpoints

---

## Contributing

Pull requests and issues are welcome! Please open an issue for feature requests or bug reports.

---

## License

This project is licensed under the GNU General Public License v3.0.  
See the [LICENSE](./LICENSE) file for details.

---

*For further details, see individual scripts and code comments. If you have specific questions, please ask!*
