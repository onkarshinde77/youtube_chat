from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from typing import List,Tuple,Dict
import sys
import os
from dotenv import load_dotenv
load_dotenv()

from src.exception.exception import CustomException
from src.logger.logger import logging
class VideoTransScript:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOOGLE_GEMINI_API_KEY")
        )
        self.api = YouTubeTranscriptApi()
        
    def get_transcripts(self,id:str):
        try:
            transcript_list = self.api.fetch(
                id,
                languages=['en']
            )
            # flatten into plain text
            transcript = " ".join(chunk.text for chunk in transcript_list)
            return transcript
        except Exception as e:
            logging.info("Occcuring error in get_transcripts function")
            raise CustomException(e,sys)

obj = VideoTransScript()
id = "RMAux-sD1bA"
result = obj.get_transcripts(id)
print(result)