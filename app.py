import streamlit as st
import os
import tempfile
import pandas as pd
import cv2
from io import BytesIO
import matplotlib.pyplot as plt

# Import custom modules
from pdf_processing import extract_text_from_pdf
from mcq_generation import generate_mcqs_and_answers
from pdf_and_csv_output import save_mcqs_to_pdf, save_answers_to_csv
from omr_processing import process_single_file

# Set up the page layout
st.set_page_config(page_title="OMR & MCQ Processing", page_icon="📝", layout="wide")

# Apply custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #ffffff;
    }
    .score-container {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .score-value {
        font-size: 4rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .score-label {
        font-size: 1.2rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("OMR and MCQ Processing System")

# Create tabs for the two main features
tab1, tab2 = st.tabs(["Generate MCQs", "Grade OMR Sheets"])

# Helper function to save uploaded file temporarily
def save_uploaded_file(uploaded_file, suffix):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return path

# ----------------- MCQ GENERATOR TAB -----------------
with tab1:
    st.header("Generate MCQs from PDF")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        num_mcqs = st.number_input("Number of MCQs to generate", min_value=1, max_value=30, value=10)
    with col2:
        pdf_file = st.file_uploader("Upload PDF Document", type=['pdf'])
        
    if st.button("Generate Questions"):
        if not pdf_file:
            st.error("Please upload a PDF file first.")
        elif not os.getenv("GROQ_API_KEY"):
            st.error("GROQ_API_KEY is not set in the environment or .env file.")
        else:
            with st.spinner("Extracting text and generating questions... This may take a moment."):
                try:
                    # Save PDF to temp file
                    pdf_path = save_uploaded_file(pdf_file, ".pdf")
                    
                    # Process
                    text = extract_text_from_pdf(pdf_path)
                    if text is None or not text.strip():
                        st.error("No text could be extracted from the provided PDF. Please ensure the PDF contains selectable text.")
                    else:
                        mcqs, answers, formatted_question_no_answer = generate_mcqs_and_answers(text, int(num_mcqs))
                        
                        # Save to temp files for downloading
                        mcq_temp_path = save_uploaded_file(pdf_file, "_questions.pdf") # Just getting a valid path
                        ans_temp_path = save_uploaded_file(pdf_file, "_answers.pdf")
                        csv_temp_path = save_uploaded_file(pdf_file, "_answers.csv")
                        
                        save_mcqs_to_pdf(mcqs, mcq_temp_path)
                        save_mcqs_to_pdf(answers, ans_temp_path)
                        save_answers_to_csv(formatted_question_no_answer, csv_temp_path)
                        
                        st.success("Successfully generated questions and answers!")
                        
                        # Provide download buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            with open(mcq_temp_path, "rb") as f:
                                st.download_button("Download Questions (PDF)", f, file_name="Questions.pdf", mime="application/pdf")
                        with col2:
                            with open(ans_temp_path, "rb") as f:
                                st.download_button("Download Answers (PDF)", f, file_name="Answers.pdf", mime="application/pdf")
                        with col3:
                            with open(csv_temp_path, "rb") as f:
                                st.download_button("Download Answer Key (CSV)", f, file_name="Answer_Key.csv", mime="text/csv")
                                
                    # Clean up
                    os.remove(pdf_path)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# ----------------- OMR GRADER TAB -----------------
with tab2:
    st.header("Grade OMR Sheets")
    
    st.info("Upload one or multiple OMR sheet images along with the correct Answer Key CSV to process them automatically.")
    
    col1, col2 = st.columns(2)
    with col1:
        omr_images = st.file_uploader("Upload OMR Sheets (Images)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    with col2:
        answer_key = st.file_uploader("Upload Answer Key (CSV)", type=['csv'])

    if st.button("Process OMR Sheets"):
        if not omr_images:
            st.error("Please upload at least one OMR image.")
        elif not answer_key:
            st.error("Please upload an Answer Key CSV.")
        else:
            with st.spinner("Processing OMR sheets..."):
                try:
                    # Save Answer Key temporarily
                    ans_key_path = save_uploaded_file(answer_key, ".csv")
                    
                    all_results_list = []
                    
                    # Process each uploaded image
                    for img_idx, img_file in enumerate(omr_images):
                        st.subheader(f"Results for: {img_file.name}")
                        img_path = save_uploaded_file(img_file, ".png")
                        
                        roll_no, total, obtained, results_df, highlighted_img = process_single_file(img_path, ans_key_path)
                        
                        all_results_list.append({
                            "File Name": img_file.name,
                            "Roll Number": roll_no,
                            "Total Marks": total,
                            "Obtained Marks": obtained
                        })
                        
                        # Display Score beautifully
                        score_html = f"""
                        <div class="score-container">
                            <div class="score-label">Final Score</div>
                            <div class="score-value">{obtained} / {total}</div>
                            <div style="color: #666; margin-top: 10px;">
                                <strong>Roll No:</strong> {roll_no}
                            </div>
                        </div>
                        """
                        
                        score_col, details_col = st.columns([1, 2])
                        with score_col:
                            st.markdown(score_html, unsafe_allow_html=True)
                        
                        with details_col:
                            with st.expander("View Detailed Answer Breakdown", expanded=False):
                                st.dataframe(results_df, use_container_width=True)
                        
                        if highlighted_img is not None:
                            with st.expander("View Processed OMR Highlight", expanded=False):
                                st.image(cv2.cvtColor(highlighted_img, cv2.COLOR_BGR2RGB), caption="Processed OMR Sheet", use_container_width=True)
                                
                        # Cleanup temp image
                        os.remove(img_path)
                        st.divider()

                    # Cleanup temp answer key
                    os.remove(ans_key_path)
                    
                    # Overall summary download
                    if len(all_results_list) > 0:
                        summary_df = pd.DataFrame(all_results_list)
                        st.success("All sheets processed successfully!")
                        st.subheader("Batch Summary")
                        st.dataframe(summary_df, use_container_width=True)
                        
                        csv_buffer = BytesIO()
                        summary_df.to_csv(csv_buffer, index=False)
                        st.download_button(
                            label="Download Batch Summary (CSV)",
                            data=csv_buffer.getvalue(),
                            file_name="OMR_Batch_Summary.csv",
                            mime="text/csv"
                        )

                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
