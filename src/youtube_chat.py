from youtube_transcript_api import YouTubeTranscriptAPI , TranscriptDisable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from typing import List,Tuple,Dict
import sys

class VideoTransScript:
    def __init__(self):
        model = ChatGoogleGenerativeAI()
        
    def get_transcripts(id:str)->List[Dict]:
        try:
            transcript_list = YouTubeTranscriptAPI.get_transcript(id,languages=['en'])
            # flatten into plain text
            transcript = " ".join(chunk['text'] for chunk in transcript_list)
        except Exception as e:
            raise CustomException(e,sys)