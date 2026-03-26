import os

from engines.providers.anthropic_provider import chamar_anthropic
from engines.providers.openai_provider import chamar_openai
from engines.providers.google_provider import chamar_google


async def executar_ai_api(prompt: str, provider: str = "openai",
                          modelo: str = None, on_progress=None) -> str:
    """Executa prospeccao via API de IA (Anthropic, OpenAI ou Google)."""

    if on_progress:
        await on_progress("enviando_prompt", 0)

    if provider == "anthropic":
        resultado = await chamar_anthropic(prompt, modelo)
    elif provider == "openai":
        resultado = await chamar_openai(prompt, modelo)
    elif provider == "google":
        resultado = await chamar_google(prompt, modelo)
    else:
        raise ValueError(f"Provider desconhecido: {provider}")

    if on_progress:
        await on_progress("resposta_recebida", 100)

    return resultado
