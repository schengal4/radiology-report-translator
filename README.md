# Oncologic Co-Pilot
Oncologic Co-Pilot is a sophisticated tool designed to assist physicians in managing oncologic surgeries. This application utilizes the ChatGPT API with a specialized prompt format to leverage Large Language Models (LLMs) in providing detailed, medically accurate responses to physician inquiries regarding various oncologic surgeries. It also features comprehensive informational content and tailored images specific to different types of oncologic procedures. Oncologic Co-Pilot aims to enhance the communication flow between surgeons and their medical teams, offering a streamlined and efficient way to access surgical information.

## Setting up the environment
To set up the environment, first create the environment: `conda create --name op_assistant`.
Then, activate the environment with `conda activate op_assistant`.
Then, to install the necessary packages, run `pip install requirements.txt`.
This app requires an OpenAI API key to run. To connect the app to your OpenAI Key, run `export OPENAI_KEY = <your_key>` in your terminal.

## Running the app
After setting up the environment, launch the application with streamlit run home_page.py. The app will prompt you to select an oncologic surgery. The resources page will then display relevant information about the chosen surgery, and the chatbot feature will be available to provide further insights into the surgical procedure. Currently, the app includes resources for procedures like Whipple surgery and radical mastectomy.

## Credits
This app is a variation that was built from Patient Co-Pilot, by Mishaal Ali MD, Kate Callon, Jennifer Xu, Edward Yap MD
