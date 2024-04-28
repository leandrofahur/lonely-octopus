import openai
import streamlit as st

# Streamlit UI components for API key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
client = openai.OpenAI(api_key=api_key)

if api_key:
    openai.api_key = api_key

    def compare_resume_to_job_description(resume_text, job_description_text):
        messages = [
        {"role": "system", "content": "You are a recruitment assistant."},
        {"role": "user", "content": f"""
            Given the following resume:
            {resume_text}
            And the following job description:
            {job_description_text}

            Identify the skills and qualifications from both.
            Then, compare them to determine any skill gaps and estimate how qualified the individual is for the job, providing a percentage.
            """
        }
        ]

        # Using the client to make the API call with streaming
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content

    st.title('ResumeFit: Compare Your Resume to Job Descriptions')
    resume_text = st.text_area("Paste Your Resume Here")
    job_description_text = st.text_area("Paste the Job Description Here")

    submit_button = st.button('Compare')
    if submit_button and resume_text and job_description_text:
        comparison_result = compare_resume_to_job_description(resume_text, job_description_text)
        st.markdown("### Comparison Results")
        st.write(comparison_result)
else:
    st.warning("Please enter your API key to proceed.")