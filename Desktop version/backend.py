from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import re
import os

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

def strip_ansi_sequences(text):
    """Remove ANSI escape sequences and other control characters from a string."""
    ansi_escape = re.compile(r'''
        \x1B[@-_][0-?]*[ -/]*[@-~]  # ANSI escape sequences
        | \x08                      # Backspace character
        | \x1B\[.*?[@-~]            # ESC sequences
        | \r\n                      # Carriage return newline
        | \r                        # Carriage return
        | \n                        # Newline
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)

@app.post("/generate")
async def generate_text(prompt: Prompt):
    print("Received request:", prompt.prompt)
    try:
        command = ["/usr/local/bin/ollama", "run", "phi3", prompt.prompt]

        env = os.environ.copy()
        env["HOME"] = os.path.expanduser("~")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            env=env
        )

        stdout, stderr = process.communicate()

        clean_stdout = strip_ansi_sequences(stdout)
        clean_stderr = strip_ansi_sequences(stderr)

        print("STDOUT:", clean_stdout)
        print("STDERR:", clean_stderr)

        if "ERROR" in clean_stderr or "error" in clean_stderr:
            raise HTTPException(status_code=500, detail=clean_stderr.strip())

        return {"text": clean_stdout.strip()}
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
