# src/analyze_readme.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def summarize_readme(readme_text):
    if not readme_text or readme_text == "README not found.":
        return "No README available to summarize."
    
    max_chars = 5000
    if len(readme_text) > max_chars:
        readme_text = readme_text[:max_chars] + "\n\n[Content truncated for summary]"

    prompt = f"Summarize this GitHub README:\n\n{readme_text}"
    return _call_groq_api(prompt)

def summarize_file(file_path, file_content):
    """
    Summarize the content of a single file.
    
    Args:
        file_path (str): Path of the file in the repo
        file_content (str): Content of the file
    
    Returns:
        str: Summary of the file's purpose
    """
    if not file_content or "Error" in file_content:
        return f"{file_path}: Unable to summarize due to fetch error or empty content."
    
    # Truncate to avoid token limits
    max_chars = 5000
    if len(file_content) > max_chars:
        file_content = file_content[:max_chars] + "\n\n[Content truncated for summary]"

    prompt = f"Summarize this file from a GitHub repository:\nFile: {file_path}\n\nContent:\n{file_content}"
    return _call_groq_api(prompt)

def _call_groq_api(prompt):
    """Helper function to call Groq API."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 200  # Shorter summary for files
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Error fetching summary: {str(e)}"