import subprocess

def run_ollama(prompt: str, model: str = "llama3") -> str:
    cmd = ["ollama", "run", model]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, _ = process.communicate(prompt)
    return output.strip()
