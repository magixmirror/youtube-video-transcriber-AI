import streamlit as st
from generate_notes import generate_text
from transcript import extract_transcript, get_yt_image
from prepare_prompt import get_prompt
import os
import base64
from PyPDF2 import PdfReader
from markdown_pdf import Section, MarkdownPdf
from langchain_community.document_loaders import PyPDFLoader
import re

from utils import generate_word_file
# Streamlit app
def main():
    st.set_page_config(
    page_title="Youtube Video Notes",
    page_icon="📹"  # You can use emoji or provide a URL to an image
    )
    credentials = True

    st.title("Youtube Video Notes")
    st.write("Note that if a video has transcriptions/subtitles then it can generate notes")
    model = st.selectbox("Select a Gen Model:", ["Select any option", "OpenAI", "Gemini Pro"], key="action_selectbox")
    # Get API key from the user
    api_key = st.text_input("Enter your API key:", type="password")
    if model=="OpenAI" and api_key:

        if not re.match(r'^sk-', api_key):
            credentials=False
            st.warning("OpenAI key is incorrect !")
    elif model=="Gemini Pro" and api_key:
        if not (re.match(r'^AI', api_key) or re.match(r'^GOCSPX-', api_key)):
            st.warning("Credentials are incorrect!")
            credentials = False
        else:
            credentials =True
            
    # Show the video URL input only when the API key is entered
    if credentials:
            video_url = st.text_input("Enter the URL of the video:")
            if video_url:
                try:
                    image=get_yt_image(video_url)
                    st.image(image)
                except Exception as e:
                    st.warning(e)

    
    # Choose action
            action = st.selectbox("Select an action:", ["Select any option", "Download Notes", "Make Report"])
            action_validated = False
            answer = None
            notes=None
            if action=="Make Report":
                transcript = extract_transcript(video_url, model=model,api_key=api_key)
                prompt = get_prompt(video_url,model=model,api_key=api_key,transcript=transcript, report=True)
                notes = generate_text(prompt=prompt , model_=model, api_key=api_key)

            # Check if "Perform Action" button is clicked
            if st.button(f'{action}'):
                if model == "OpenAI":
                    os.environ["OPENAI_API_KEY"] = api_key
                else:
                    os.environ['GOOGLE_API_KEY'] = api_key

                # Perform action based on the selected option
                if action == "Download Notes":
                    pdf = MarkdownPdf(toc_level=2)
                    st.write("Downloading notes...")
                    transcript = extract_transcript(video_url, model=model,api_key=api_key)
                    prompt = get_prompt(video_url,model=model,api_key=api_key ,transcript=transcript)
                    
                    notes = generate_text(prompt=prompt, model_=model,api_key=api_key)

                    # Display notes in Markdown format
                    st.markdown(notes, unsafe_allow_html=True)

                    pdf.add_section(Section(notes,toc=False))

                    st.write(f"Notes converted to PDF. You can download the PDF below.")
                    file_path = "notes_.pdf"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    pdf.save(file_path)
                    download_button_style = "padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;"
                    download_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open(file_path, "rb").read()).decode("utf8")}" download="notes.pdf" style="{download_button_style}">Download PDF</a>'

                    st.markdown(download_link, unsafe_allow_html=True)


                # Add code to initiate chat with notes here
                elif action == "Make Report":
                    if notes is not None:
                        st.write("Wait , We are generating your report")
                        generate_word_file(notes, "report.docx")
                        st.success("Your report is generated , You can download it !")
                        download_button_style = "padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;"
                        download_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open("report.docx", "rb").read()).decode("utf8")}" download="report.docx" style="{download_button_style}">Download Report</a>'
                        st.markdown(download_link, unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()
