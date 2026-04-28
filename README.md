# OMR and MCQ Generation System

A streamlined, web-based system that automates the generation of Multiple Choice Questions (MCQs) from PDF documents and the grading of Optical Mark Recognition (OMR) sheets. Built with Python and Streamlit, this application provides an intuitive and modern interface for educators and examiners.

## 🚀 Features

### 1. MCQ Generation from PDF
- Upload any text-based PDF document.
- AI-powered extraction of MCQs and their answers using the Groq API.
- Specify the exact number of questions you want to generate.
- Download the generated questions as a PDF and the answer key as a CSV or PDF.

### 2. OMR Sheet Processing
- Upload single or multiple scanned OMR sheets (PNG/JPG).
- Upload an answer key in CSV format.
- Automated optical mark recognition using OpenCV to detect and evaluate filled answers.
- Visually highlights detected answers on the processed sheets.
- Provides a clear `score / total` grading summary.
- Export detailed batch processing results to a CSV report.

## 🛠️ Technologies Used

- **Frontend:** Streamlit (Web UI)
- **Image Processing:** OpenCV, NumPy
- **AI/LLM API:** Groq API
- **Data Handling:** Pandas
- **PDF Processing:** PyPDF2, ReportLab
- **Environment Management:** Python `python-dotenv`

## ⚙️ Installation & Setup (Windows)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FarooqK-Nu/OMR-and-MCQ-Generation-System.git
   cd OMR-and-MCQ-Generation-System
   ```

2. **Create a Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Copy `.env.example` to `.env`:
     ```powershell
     cp .env.example .env
     ```
   - Open the `.env` file and add your `GROQ_API_KEY`.

## 🏃‍♂️ Running the Application

Start the Streamlit application by running the following command in your activated virtual environment:

```powershell
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## 📝 Usage Guide

### Generating MCQs
1. Open the **"Generate MCQs"** tab.
2. Upload a text-readable PDF.
3. Select the desired number of questions.
4. Click **"Generate Questions"**.
5. Download the resulting PDF and CSV answer key.

### Grading OMR Sheets
1. Open the **"Grade OMR Sheets"** tab.
2. Upload your scanned OMR images (you can select multiple files at once).
3. Upload the correct Answer Key CSV (format: `question_no,answer`).
4. Click **"Process OMR Sheets"**.
5. Review the visual highlights, individual scores, and download the batch summary report.

## 🤝 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
