from flask import Flask, request, render_template, jsonify
from langchain_mistralai import ChatMistralAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

system_prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
with heading. Please provide the summary of the text given here:  """

def get_video_id(url):
    video_id = url.split("/")[3]
    return video_id

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    final = "\n".join(item["text"] for item in transcript)
    return final

def get_summary(final):
    prompt = system_prompt + final
    llm = ChatMistralAI(model_name="mistral-large-latest")
    result = llm.invoke(prompt)
    return result.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        video_id = get_video_id(url)
        transcript = get_transcript(video_id)
        summary = get_summary(transcript)
        return render_template('index.html', summary=summary)
    return render_template('index.html', summary=None)

if __name__ == '__main__':
    app.run(debug=True)