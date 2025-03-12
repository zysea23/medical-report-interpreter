# Medical Report Interpreter

## Overview
**Medical Report Interpreter** is an **on-device AI** application built with FastAPI. It enables users to upload medical report images, extract structured text, provide user-friendly explanations, and support translation and Q&A functionalities. The system runs entirely **locally**, ensuring privacy and security. It integrates **LMStudio** for local AI processing using the **Qwen2-VL-2B-Instruct** model.

![example1](example/screenshoot1.png)
![example2](example/screenshoot2.png)

## Project Structure
```
medical-report-interpreter/
│
├── app/
│   ├── main.py                  # FastAPI main application
│   ├── models/lm_handler.py     # Handles LMStudio API interactions
│   └── services/report_service.py  # Medical report processing service
│
├── static/                      # Frontend assets
├── templates/                   # HTML templates
├── uploads/                     # Uploaded file storage
│
├── .env                         # Environment variables
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## How to Set Up LMStudio
1. **Download and Install LMStudio**
   - Get LMStudio from: [https://lmstudio.ai](https://lmstudio.ai)

2. **Load the Model**
   - Download **Qwen2-VL-2B-Instruct** from Hugging Face.
   - In LMStudio, load `Qwen2-VL-2B-Instruct` and ensure it is running on port `1234`.

3. **Configure LMStudio for Local API Access**
   - Go to `Settings` in LMStudio.
   - Enable `Local API` and set the endpoint to `http://localhost:1234/v1/chat/completions`.

## How to Run

### 1. Set Up Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

Ensure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Start the Application

```bash
python -m app.main
```

### 4. Access the Web Interface

Open the following URL in a browser:

```
http://localhost:8000
```

### 5. Upload and Analyze a Medical Report

- Navigate to the home page and upload a medical report image (`.jpg`, `.jpeg`, `.png`).
- The system will extract text and structure, providing an explanation of medical terms.

### 6. Translation

- Click the **Translate** button to convert the explanation into another language (default: Chinese).

### 7. Ask Medical Questions

- Enter a question related to the extracted report content and receive AI-generated answers.

### 8. API Endpoints

You can interact with the system via API:

- **`POST /upload`** – Upload a medical report image for analysis.
- **`POST /translate`** – Translate extracted report content.
- **`POST /ask`** – Ask medical-related questions based on extracted data.


## Future Work
### 1. **Runtime**
- Migrate from LMStudio's local LLM API to **ONNX Runtime**, enabling more efficient execution and compatibility with different hardware, including **Snapdragon-based** devices.

### 2. Function
- Implement **local storage** for user history to enable further retrieval and personalized interactions.
- Integrate **RAG (Retrieval-Augmented Generation)** by searching a local vector database for relevant context before generating explanations and answers.
- Expand translation support to **more languages** beyond Chinese.
- Support voice input and output, allowing users to interact via speech recognition and text-to-speech synthesis.

### 3. Model
- Replace **Qwen2-VL-2B-Instruct** with a **larger and more powerful model**, if resources allow, to enhance processing accuracy.
- Utilize a **domain-specific fine-tuned model** for improved medical interpretation, Q&A, and translation (if the model supports it).
- Refine the prompt to ensure more accurate and relevant explanations and responses.

### 4. Frontend & Backend
- Improve the **frontend UI/UX** to provide a more intuitive and visually appealing experience.
- Enhance the **backend architecture** to improve stability, scalability, and maintainability.

### 5. Testing
- Find and use **real medical report images** to enhance model evaluation and ensure accuracy.
