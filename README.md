# Teachable Machine

A web application for building custom image classification models without coding. Train your own image classifier by uploading samples and make predictions through an intuitive interface.

## Features

- **Easy Model Training**: Upload images organized by category to train a custom classifier
- **Fast Inference**: Real-time predictions on new images
- **Clean UI**: Dark-themed Streamlit frontend with a responsive design
- **REST API**: FastAPI backend for programmatic access
- **Pre-trained Models**: Uses MobileNetV3 for efficient feature extraction

## Project Structure

```
├── backend/                # FastAPI server
│   ├── main.py            # API endpoints and model logic
│   ├── requirements.txt    # Python dependencies
│   └── dataset/           # Training images (organized by class)
│       ├── cat/
│       └── dog/
└── frontend/              # Streamlit web interface
    └── app.py             # User-facing application
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

### Running the Application

**Terminal 1 - Start the Backend:**
```bash
cd backend
uvicorn main:app --reload
```
Backend will run on `http://localhost:8000`

**Terminal 2 - Start the Frontend:**
```bash
cd frontend
streamlit run app.py
```
Frontend will open at `http://localhost:8501`

## How to Use

1. **Prepare Training Data**: Add image files to folders in `backend/dataset/` named after each class (e.g., `cat/`, `dog/`)
2. **Train a Model**: Use the frontend interface to load and train on your dataset
3. **Make Predictions**: Upload new images to see predictions from your trained model

## Tech Stack

- **Backend**: FastAPI, PyTorch, scikit-learn, Pillow
- **Frontend**: Streamlit, Requests, Pandas
- **ML Models**: MobileNetV3 (feature extraction), Logistic Regression (classification)

## API Endpoints

- `POST /upload` - Upload and train on image dataset
- `POST /predict` - Make predictions on new images

## Requirements

See `backend/requirements.txt` for all Python packages.
