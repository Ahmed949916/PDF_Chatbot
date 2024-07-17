import sys
from PyQt5 import QtWidgets, uic
import requests

class PdfAIApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(PdfAIApp, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.selectFileButton.clicked.connect(self.select_file)
        self.triggerButton.clicked.connect(self.trigger_interaction)
        self.pdf_file_path = None
        self.pdf_text = ""  # Initialize PDF text as empty string
        self.history = []  # Initialize an empty list to store history

    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select PDF Document", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.pdf_file_path = fileName
            self.pdfPathLineEdit.setText(fileName)
            self.pdf_text = self.extract_text_from_pdf(fileName)

    def trigger_interaction(self):
        user_input = self.queryTextEdit.toPlainText()
        questions = user_input.split('\n')  # Assuming each question is on a new line
        current_text = self.outputTextEdit.toPlainText()  # Get the current text from the output text edit
        responses = []
        for question in questions:
            if question.strip():  # Make sure the question is not just whitespace
                response = self.process_with_llm(question, self.pdf_text)
                self.history.append((question, response))  # Add to history
                responses.append(f"Q: {question}\nA: {response}\n")
        if current_text:
            updated_text = f"{current_text}\n{''.join(responses)}"
        else:
            updated_text = "\n".join(responses)
        self.outputTextEdit.setPlainText(updated_text)  # Set the updated text

    def extract_text_from_pdf(self, pdf_path):
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def process_with_llm(self, user_input, pdf_text):
        # Format the history for sending
        history_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])
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

app = QtWidgets.QApplication(sys.argv)
window = PdfAIApp()
window.show()
sys.exit(app.exec_())
