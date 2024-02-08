import os
import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
#from google.colab import userdata

# Load environment variables
load_dotenv()

# Configure the Google Generative AI with your API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#genai_api_key = os.getenv("GOOGLE_API_KEY")
#genai.configure(api_key=genai_api_key)

# Define the prompt for the model
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract video ID from various URL formats
def extract_video_id(youtube_video_url):
    if "youtu.be" in youtube_video_url:
        video_id = youtube_video_url.split("/")[-1]
    else:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]
    return video_id

# Function to extract transcript and generate summary
def youtube_to_notes(youtube_video_url):
    video_id = extract_video_id(youtube_video_url)

    # Extracting transcript from the YouTube video
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
    except Exception as e:
        return f"Failed to extract transcript: {e}"

    # Generating summary using Google Gemini Pro
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        summary = response.text
        return summary
    except Exception as e:
        return f"Failed to generate summary: {e}"

# Building the Gradio Blocks interface
with gr.Blocks() as demo:
    gr.Markdown("# 🅱🅻🅰🆀's YouTube Video Summarizer")
    #gr.Title("🅱🅻🅰🆀's YouTube Video Summarizer")
    youtube_link = gr.Textbox(label="Enter YouTube Video Link:", lines=2, placeholder="Paste your YouTube link here")
    generate_notes_btn = gr.Button("Summarize Video")
    detailed_notes = gr.Textbox(label="Video Summary", interactive=False, lines=20)

    generate_notes_btn.click(fn=youtube_to_notes, inputs=youtube_link, outputs=detailed_notes)

# Launch the interface
demo.launch(share=True, debug=True)