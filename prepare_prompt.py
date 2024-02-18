from generate_notes import generate_text
from pytube import YouTube
def get_video_title(url):
    try:
        # Create a YouTube object
        youtube = YouTube(url)

        # Access the video title
        title = youtube.title
        return title
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return None
def get_prompt(url, model,transcript,api_key,report=False):
    video_title = get_video_title(url)
    prompt =f'''
    I will give you the title of a youtube video , your work is to suggest a name for the profession , Give only name in result
    for example 
    VIDEO_TITLE: What is machine learning ?
    PROFESSION: Machine Learning Engineer
    VIDEO_TITLE: How to get a job in data science ?
    PROFESSION: Data Scientist
    VIDEO_TITLE: {video_title}
    PROFESSION: <GIVE_PROFESSION>
    '''
    profession = generate_text(prompt, model_=model,api_key=api_key)
    if report:
        prompt_final=f'''
        Act as a professional report writer and make a technical report by analyzing the transcript, Your report should contain the table of content , primary headings and seconday headings. Each heading in the table of content should be explained , primary heading "#" will be bold , And most important generate the report in markdown format
        Here is the transcript: " {transcript} ", Generated Report:  
        '''

    else:
        prompt_final=f'''
        Act as a professional {profession}, and analyze this text which is youtube transcript and make detailed notes in markdown format , Your notes should strive to provide a comprehensible grasp of both the theoretical underpinnings and real-world applications of the concepts covered in the transcript.Every heading should be explained and every good concept should be highlighted, underlined and bold , Note there should be pure markdown generated that contains No extra symbols.Don't use this symbol in that markdown "o".Make comprehensive notes.There should be a primary heading then secondary heading and then explain the secondary heading.
        "Here is the transcript: " {transcript} ", Generated Notes:  
        '''
    return prompt_final
