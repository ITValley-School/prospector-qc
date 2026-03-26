import os
import httpx


async def enriquecer_lead(website: str) -> dict:
    """Usa Firecrawl para extrair dados de um website."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY nao configurada")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "url": website,
                "formats": ["markdown"],
            },
        )
        response.raise_for_status()
        return response.json()
