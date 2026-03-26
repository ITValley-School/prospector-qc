import os
from openai import AsyncOpenAI


async def chamar_openai(prompt: str, modelo: str = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY nao configurada")

    client = AsyncOpenAI(api_key=api_key)
    modelo = modelo or "gpt-4o"

    response = await client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Voce e um especialista em prospeccao B2B. Responda sempre em JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4096,
    )

    return response.choices[0].message.content
