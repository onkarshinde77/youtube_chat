from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api._transcripts import FetchedTranscript 
from typing import List,Tuple,Dict
import sys
import os
from dotenv import load_dotenv
load_dotenv()

from src.exception.exception import CustomException
from src.logger.logger import logging
from src.logger.logger import logging


class VideoTransScript:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOOGLE_GEMINI_API_KEY")
        )
        self.api = YouTubeTranscriptApi()
        self.embedding = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        
    def get_transcripts(self,id:str):
        try:
            transcript_list = self.api.fetch(id,languages=['en'])
            # flatten into plain text
            text = " ".join(chunk.text for chunk in transcript_list)
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_text(text=text)
            return chunks
        
        except Exception as e:
            logging.info("Occcuring error in get_transcripts function")
            raise CustomException(e,sys)

    # generating embedding and storing in vectorstore (indexing)
    def emedding_store(self,id:str):
        try:
            chunks = self.get_transcripts(id=id)            
            docs = [Document(page_content=chunk) for chunk in chunks]
            # vector = self.embedding.embed_query(chunks)   
            vector_store = FAISS.from_documents(docs,self.embedding)
            # print(vector_store.index_to_docstore_id)
            return vector_store
        
        except Exception as e:
            raise CustomException(e,sys)



id = "RMAux-sD1bA"
obj = VideoTransScript()
vector_db = obj.emedding_store(id=id)
print("Stored vector : " , vector_db.index_to_docstore_id)

