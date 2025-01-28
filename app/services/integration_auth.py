# integration_auth.py
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..config import Settings

class IntegrationAuth:
    def __init__(self):
        self.settings = Settings()

    async def handle_oauth(self, provider: str, code: str, db: Session):
        handlers = {
            'zoom': self._handle_zoom_oauth,
            'teams': self._handle_teams_oauth
        }
        
        handler = handlers.get(provider)
        if not handler:
            raise HTTPException(400, f"Unsupported provider: {provider}")
            
        return await handler(code, db)

    async def _handle_zoom_oauth(self, code: str, db: Session):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://zoom.us/oauth/token',
                data={
                    'code': code,
                    'grant_type': 'authorization_code',
                    'client_id': self.settings.zoom_client_id,
                    'client_secret': self.settings.zoom_client_secret
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(400, "Failed to get Zoom token")
                
            return response.json()
