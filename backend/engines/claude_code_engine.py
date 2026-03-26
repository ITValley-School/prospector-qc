import os
import json
import asyncio


async def executar_claude_code(prompt: str, on_progress=None) -> str:
    """Executa o Claude Code CLI como subprocess e retorna o resultado."""
    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "json",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    stdout_data = b""
    while True:
        chunk = await process.stdout.read(4096)
        if not chunk:
            break
        stdout_data += chunk
        if on_progress:
            await on_progress("processando", len(stdout_data))

    await process.wait()

    if process.returncode != 0:
        stderr = await process.stderr.read()
        raise RuntimeError(f"Claude Code falhou (exit {process.returncode}): {stderr.decode()}")

    output = stdout_data.decode("utf-8").strip()

    # Parse JSON output from claude CLI
    try:
        result = json.loads(output)
        if isinstance(result, dict) and "result" in result:
            return result["result"]
        if isinstance(result, dict) and "content" in result:
            return result["content"]
        return output
    except json.JSONDecodeError:
        return output
