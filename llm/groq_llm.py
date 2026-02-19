import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(override=True)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def explain_match(field, resume_text, jd_text):
    prompt = f"""
You are an ATS AI.

Compare resume and job description for {field}.

Return ONLY valid JSON in this format:
{{
  "explanation": "short explanation of match or mismatch"
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)

        # ✅ HANDLE LIST RESPONSE
        if isinstance(data, list):
            data = data[0] if data else {}

        return data.get(
            "explanation",
            "No explanation returned by the model."
        )

    except json.JSONDecodeError:
        # fallback if model breaks JSON
        return response.content.strip()
