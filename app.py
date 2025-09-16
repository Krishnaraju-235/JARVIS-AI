from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment. Please set it in a .env file.")

base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
model = "gemini-2.5-flash"
client = OpenAI(base_url=base_url, api_key=api_key)

def load_file_content(file_path):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        if file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return "\n".join([line.strip() for line in f if line.strip()])
        elif file_path.lower().endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                pages_text = [page.extract_text().strip() for page in reader.pages if page.extract_text()]
                return "\n".join(pages_text) if pages_text else "No text found in PDF"
        else:
            return f"Unsupported file type: {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def build_context(file_paths):
    contexts = []
    for path in file_paths:
        file_content = load_file_content(path)
        contexts.append(f"--- Content from {os.path.basename(path)} ---\n{file_content}")
    return "\n\n".join(contexts)

def get_response(message, history, file_paths, context_only=False):
    combined_context = build_context(file_paths)
    if combined_context.strip():
        if context_only:
            system_prompt = f"""You are Jarvis AI, an AI assistant.
Answer the user's question based ONLY on the following context:
{combined_context}
"""
        else:
            system_prompt = f"""You are Jarvis AI, an AI assistant.
Use the provided context to answer user questions.
If the context does not contain relevant information,
then answer from your own knowledge.
Context:
{combined_context}
"""
    else:
        system_prompt = "You are Jarvis AI, an AI assistant. Answer freely using your knowledge."

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content