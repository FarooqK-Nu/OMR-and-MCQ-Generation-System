import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_mcqs_and_answers(input_text, num_mcqs):
    #Generate multiple-choice questions (MCQs) and their answers using the Groq API.
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing or not set in the environment.")

    # Initialize the Groq client
    client = Groq(api_key=api_key)
    try:
        # Validate the number of MCQs
        if num_mcqs <= 0:
            raise ValueError("Number of MCQs must be a positive integer.")

        # Step 1: Generate MCQs without answers
        mcq_prompt = (
            f"Generate {num_mcqs} multiple-choice questions without answers "
            f"based on the following text:\n\n{input_text}"
        )

        # Request MCQs from the API
        mcq_response = client.chat.completions.create(
            messages=[{"role": "user", "content": mcq_prompt}],
            model="llama-3.1-8b-instant"
        )

        if not mcq_response.choices:
            raise RuntimeError("No MCQs were returned from the API.")

        # Extract and process the MCQs
        mcqs = mcq_response.choices[0].message.content.strip().split("\n")

        #Step 2: Generate answers for the MCQs
        # Generate answers for the MCQs
        prompt_answers = f"Provide the correct answers to the following multiple-choice questions:\n\n{mcqs}"

        # Use Groq's chat completion API to generate the answers
        answer_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_answers
                }
            ],
            model="llama-3.1-8b-instant"
        )

        if not answer_response.choices:
            raise RuntimeError("No answers were returned from the API.")

        # Extract and process the answers
        answers = answer_response.choices[0].message.content.strip().split("\n")
        prompt_question_no_answer = f"Format the following answers into a CSV-like list with question_no and answer (no text, no formatting, just:\n\nquestion_no,answer\n1,a\n2,b\n...):\n\n{answers}"

        formatted_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_question_no_answer
                }
            ],
            model="llama-3.1-8b-instant"
        )

        if not formatted_response.choices:
            raise RuntimeError("No formatted data was returned from the API.")

        # Extract and process the formatted output
        formatted_output = formatted_response.choices[0].message.content.strip()
        formatted_lines = formatted_output.split("\n")

        # Parse the formatted lines into a list of (question_no, answer) tuples
        question_no_answer = []
        for line in formatted_lines:
            if "," in line and line.split(",")[0].strip().isdigit():
                question_no, answer = line.split(",", 1)
                question_no_answer.append((int(question_no.strip()), answer.strip()))

        # Return the generated MCQs, answers, and formatted data
        return mcqs, answers, question_no_answer

    except ValueError as value_error:
        raise ValueError(f"Value error: {value_error}") from value_error
    except RuntimeError as runtime_error:
        raise RuntimeError(f"Runtime error: {runtime_error}") from runtime_error
    except Exception as exception:
        raise RuntimeError(f"An unexpected error occurred during MCQ generation: {exception}") from exception


