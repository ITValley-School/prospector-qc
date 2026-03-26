import os
import anthropic


async def chamar_anthropic(prompt: str, modelo: str = None) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY nao configurada")

    client = anthropic.AsyncAnthropic(api_key=api_key)
    modelo = modelo or "claude-sonnet-4-20250514"

    response = await client.messages.create(
        model=modelo,
        max_tokens=4096,
        system="Voce e um especialista em prospeccao B2B. Responda sempre em JSON.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.content[0].text
