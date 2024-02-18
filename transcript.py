from youtube_transcript_api import YouTubeTranscriptApi
from generate_notes import generate_text
from prepare_prompt import get_prompt
import streamlit as st
'''
Extracting the youtube scripts
'''
def extract_transcript(youtube_url:str, model,api_key)->str:
    '''
    https://pypi.org/project/youtube-transcript-api/
    You can visit this link to check the documentation


    https://www.youtube.com/watch?v=12345667
    This is sample video note that we have to obtain the id i.e after v=
    so lets get started
    '''
    try:
        yt_id=youtube_url.split('=')[-1]
        transcript = YouTubeTranscriptApi.get_transcript(yt_id)
        image_url=f"http://img.youtube.com/vi/{yt_id}/0.jpg"
        if transcript:  
            '''
            We will obtain the result in a dictionary, so we will filter out the the text
            '''
            text=""
            for txt in transcript:
                text += ' ' + txt['text']
            prompt = get_prompt(youtube_url,transcript=text,api_key=api_key ,model=model)
            notes = ""
            notes = generate_text(prompt=prompt, model_=model) 
            return notes, image_url
    except Exception as e:
        st.warning("Ooops :( ,No transcription is available for your video !")
        st.error(e)
        st.stop()
#  , ""
    
def get_yt_image(url:str):
    yt_id=url.split('=')[-1]
    transcript = YouTubeTranscriptApi.get_transcript(yt_id)
    image_url=f"http://img.youtube.com/vi/{yt_id}/0.jpg"
    return image_url