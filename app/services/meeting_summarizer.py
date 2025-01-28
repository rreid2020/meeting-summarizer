# meeting_summarizer.py
import whisper
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from fastapi import HTTPException
import tempfile
from ..config import Settings

class MeetingSummarizerService:
    def __init__(self):
        settings = Settings()
        self.model = whisper.load_model("tiny")
        self.llm = OpenAI(openai_api_key=settings.openai_api_key)

    async def process_meeting(self, file):
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
                temp_file.write(file.read())
                temp_file.flush()
                
                result = self.model.transcribe(temp_file.name)
                return {
                    "transcription": result["text"],
                    "duration": result["duration"]
                }
        except Exception as e:
            raise HTTPException(500, f"Error processing meeting: {str(e)}")

    async def _extract_actions(self, text: str):
        prompt = f"Extract action items from this text: {text}"
        response = await self.llm.agenerate([prompt])
        return response.generations[0].text.split('\n')