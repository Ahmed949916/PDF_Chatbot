import streamlit as st
import requests
import pdfplumber

def extract_text_from_pdf(pdf):
    text = ""
    with pdfplumber.open(pdf) as pdf_doc:
        for page in pdf_doc.pages:
            text += page.extract_text() or ""
    return text

def process_with_llm(user_input, pdf_text, history):
    history_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    url = "http://127.0.0.1:8000/generate"
    prompt = f"User question: {user_input}"
    if pdf_text:
        prompt += f"\nPDF content: {pdf_text[:10000]}"  # Include PDF text if available
    prompt += f"\nHistory:\n{history_text}"
    data = {"prompt": prompt}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("text", "No answer found in response.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the LLM server: {e}"

def main(history):
    st.title("PDF AI Interaction App")

    pdf_file_path = None
    pdf_text = ""

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF uploaded successfully!")

    user_input = st.text_area("Enter your question:")

    if st.button("Send"):
        if user_input.strip():
            response = process_with_llm(user_input, pdf_text, history)
            history.append((user_input, response))

    st.subheader("Chat History")
    for i, (question, answer) in enumerate(history):
        st.write(f"**User:** {question}")
        st.write(f"**AI:** {answer}")

if __name__ == "__main__":
    history = []
    main(history)
