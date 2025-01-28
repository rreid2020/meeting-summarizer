# meeting_summarizer.py
import whisper
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document

class MeetingSummarizerService:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.llm = OpenAI()

    async def process_meeting(self, audio_file):
        # Transcribe
        result = self.model.transcribe(audio_file)
        
        # Summarize
        docs = [Document(page_content=result["text"])]
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        summary = chain.run(docs)
        
        # Extract action items
        actions = await self._extract_actions(result["text"])
        
        return {
            "summary": summary,
            "action_items": actions,
            "duration": result.get("duration", 0)
        }

    async def _extract_actions(self, text: str):
        prompt = f"Extract action items from this text: {text}"
        response = await self.llm.agenerate([prompt])
        return response.generations[0].text.split('\n')