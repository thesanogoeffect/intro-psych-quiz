# Intro to Psychology Questions

This project aims to create a centralized repository of multiple-choice questions for psychology students, using questions sourced from various contributors. The goal is to provide an interactive platform where students can practice, review, and contribute questions based on the OpenStax Psychology book.

**Current Question Collection:**  
Questions are currently collected in a collaborative [Google Doc](https://docs.google.com/document/d/14OcbX4qMwhRGgL2HfmaO_qIqZKjJfzWfvDCaZ8Kxpaw/edit).

## Plans for Development

This project is being actively developed into an interactive web app using **Streamlit** and may potentially be migrated to **Vue.js** in the future for enhanced interactivity. Below is the development plan.

### Database Structure

The project will utilize multiple database layers to organize and refine the quality of questions. The database layers are outlined as follows:

- **L1 - Raw Questions**: All obtained questions, including:
  - **Source**: Indicates where the question originated (e.g., Google Form, previous years' questions, Google Doc, OpenStax).
  - **Author**: Contributor of the question.
  - **Email**: Contact email of the contributor (for follow-up if needed).
  - **Date**: Date the question was submitted.

- **L2 - Initial Validation**: All questions, enriched with validation data:
  - `is_format_valid?`: Checks if the question meets basic format requirements (e.g., has four different answer choices).
  - `is_correct_chapter?`: Verifies if the question is relevant to the indicated chapter.
  - `is_question_correct?`: Checks if the question itself is factually correct.
  - `is_sufficient?`: Assesses if the question quality is sufficient to move forward in the pipeline.

- **L3 - Verified Questions**: Contains only the questions that have passed the validation checks. This includes all necessary metadata (correct formatting, grammar, chapter relevance).

- **L4 - Quality-Rated Questions**: Questions enriched with:
  - **Quality Ratings**: Provided by both users and Language Learning Models (LLMs).
  - **Difficulty Ratings**: Based on LLM analysis and user feedback.

- **L5 - Final Set**: The set of questions available for student practice, including:
  - Only those questions that exceed a certain quality score.
  - Excludes duplicates (retains only the highest-quality version of any duplicate question).

### Processing Pipeline

The app will employ a multi-step pipeline for validating and improving the quality of submitted questions:

1. **Step 1: Format Validation**  
   - Check if the question has four distinct answers and makes general sense.
   - **If not:** Discard the question or attempt an automated fix if possible.

2. **Step 2: Chapter Relevance**  
   - Verify if the question pertains to the indicated chapter.
   - **If not:** Reassign the question to the correct chapter if applicable; otherwise, discard.

3. **Step 3: Quality Assessment**  
   - Check if the question is well-phrased, clear, and has effective distractors.
   - **If not:** Attempt to fix or rephrase the question, or discard if it cannot be improved.

### Duplicate Check

- **Step 1:** Identify if a question is a direct duplicate of another in the database.
  - **If yes:** Retain the version with the highest quality score and discard the others.

### Additional Features

- **Report Question Form:**  
  Implement a form allowing users to report problematic questions, ensuring continuous improvement and curation of the question bank.

- **5-Star Review System:**  
  After answering a question, users can rate it on a 5-star scale, providing valuable quality feedback that contributes to the question's rating in **L4** and influences its inclusion in the final set in **L5**.

### Ideas and Future Enhancements

- **Make Google Doc Read-Only:** To prevent accidental edits or deletions, the Google Doc containing the raw questions will be made read-only.
- **"Yoink" Mechanism:** Finding a way for DL to source questions from database without revealing which questions are being used for the test

### Hosting and Backend

- The app will use a **hosted PostgreSQL database** for managing the different layers of questions, ensuring robust data storage and scalability.
- The initial app is being developed using **Streamlit**, with potential plans to migrate to **Vue.js** for better interactivity and user experience.
- The backend will handle data processing, validation checks, and interactions with the database, leveraging frameworks such as **Flask** or **FastAPI**.

### Technologies and Tools

- **Streamlit**: For the initial development of the web app.
- **Vue.js** (Planned): For enhanced interactivity in future versions.
- **PostgreSQL**: Hosted database for managing question data.
- **Flask/FastAPI**: Backend frameworks for processing and managing data.
- **LLMs (Language Learning Models)**: For automated quality checks and ratings.

---

This README provides an overview of the project's current state and future direction. Contributions and suggestions are welcome as we work toward building a comprehensive study tool for psychology students.
