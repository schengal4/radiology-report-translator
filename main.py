import streamlit as st
from io import BytesIO
from docx import Document
import fitz
from openai import OpenAI
from fpdf import FPDF
OPTIMIZED_PROMPT = """
Please help translate the following radiology report into plain language at a 6th grade reading level in the following format:

- First paragraph introduces screening description including reason for screening, screening time, protocol, patient background, and comparison date;
- Second paragraph talks about specific findings: how many nodules detected, each lung nodule’s precise position and size, findings on lungs, heart, pleura, coronary artery calcification, mediastinum/hilum/axilla, and other findings. Please don’t leave out any information about findings;
- Third paragraph talks about conclusions, including overall lung-rads category, management recommendation and follow-up date, based on lesion;
- If there are incidental findings, please introduce in the fourth paragraph.

"""

OPENAI_KEY = "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"
def read_docx(file):
    with BytesIO(file.read()) as doc_file:
        document = Document(doc_file)
        result = "\n".join([para.text for para in document.paragraphs])
        Document.close()
        return result
def initialize_session_state():
    if "input_choice" not in st.session_state:
        st.session_state["input_choice"] = None
    if "prev_uploaded_file" not in st.session_state:
        st.session_state["prev_uploaded_file"] = None
    if "downloaded_file" not in st.session_state:
        st.session_state["downloaded_file"] = False
def text_from_pdf_file(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text

@st.cache_data
def translate_radiology_report(report_text_in):
    client = OpenAI(api_key=OPENAI_KEY)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo", # Change later
    messages=[
        {"role": "user", "content": OPTIMIZED_PROMPT + "\n" + report_text_in}
    ]
    )
    return completion.choices[0].message.content
    
def instructions():
    st.markdown("""
    Translates a radiology report into plain language using OpenAI's GPT-4 model. More details can be found in the paper https://arxiv.org/abs/2303.09038.
    When the authors prompted ChatGPT (GPT-4 version) to translate radiology reports, GPT-4 (with the optimized prompt) clearly and accurately translated 96.8% of them.
    """)
    st.markdown("""
    ### Instructions  
    1. Paste the text of the radiology report into the text box below OR upload a .pdf or word file.  
        - Note that the OpenAI API isn't HIPAA-compliant; so, any text or documents uploaded must be \
        HIPAA-compliant and not have any identifying information or information that could be used to \
        identify the patients.  
        - The paper focused on radiology reports from chest CT lung cancer screening scans and brain MRI \
        metastases screening scans. Although other kinds of radiology reports could be translated via \
        this app, this wasn't validated in the paper.
    2. The translated report will be displayed on the screen.  
        - Although GPT-4 has impressive \
        performance on many tasks and is dramatically improved compared to GPT-3 or 3.5, it's still prone \
        to halluciations and occassionally producing inaccurate/incorrect information.
        - Also, the paper used GPT-4 via ChatGPT while this app uses GPT-4 via the API, which has been reported by some users to be performing differently.
    """)
    pass


@st.cache_data
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = BytesIO()
    pdf.output(pdf_output, 'F')
    pdf_output.seek(0)
    return pdf_output


def main():
    st.title('Radiology Report Translator')
    initialize_session_state()
    instructions()

    input_choice = st.radio("Choose your input method:", ('Paste Text', 'Upload File (beta)'), horizontal=True)
    st.session_state["input_choice"] = input_choice

    if input_choice == 'Paste Text':
        report_text = st.text_area("Paste your radiology report here. After pasting it, press ctrl + Enter and then press 'Translate report':", key="text_area")
    else:
        uploaded_file = st.file_uploader("Upload a radiology report file:", type=['txt', 'pdf', 'docx'], key="file_uploader")
        if uploaded_file is not None:
            st.session_state["prev_uploaded_file"] = uploaded_file
            if uploaded_file.type == "text/plain":
                report_text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                report_text = text_from_pdf_file(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                report_text = read_docx(uploaded_file)
            else:
                st.error("Unsupported file type" + " file type is " + str(uploaded_file.type))

    translate_button = st.button("Translate report")
    if translate_button:
        st.session_state["translated_report"] = translate_radiology_report(report_text)

    if "translated_report" in st.session_state and st.session_state["translated_report"]:
        st.subheader("Translated Report")
        st.markdown("**Below is the radiology report translated into plain language.**")
        st.markdown(st.session_state["translated_report"])

        # PDF creation and download
        pdf = create_pdf(st.session_state["translated_report"])
        download_btn = st.download_button(label="Download Translated Report as PDF",
                                          data=pdf,
                                          file_name="translated_report.pdf",
                                          mime="application/pdf")

if __name__ == "__main__":
    main()