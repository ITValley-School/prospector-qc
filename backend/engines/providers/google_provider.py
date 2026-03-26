import asyncio
import os
from google import genai


async def chamar_google(prompt: str, modelo: str = None) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY nao configurada")

    client = genai.Client(api_key=api_key)
    modelo = modelo or "gemini-2.0-flash"

    response = await asyncio.to_thread(
        client.models.generate_content,
        model=modelo,
        contents=f"Voce e um especialista em prospeccao B2B. Responda sempre em JSON.\n\n{prompt}",
    )

    return response.text
