import json
from groq import Groq

from backend.config.settings import GROQ_API_KEY


def analyze_resume(resume_text):
    """
    Uses AI to analyze resume text and convert it
    into structured candidate information.
    """

    if not resume_text or not resume_text.strip():
        return {
            "success": False,
            "data": None,
            "error": "Resume text is empty."
        }

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an expert AI resume analyzer.

Analyze the following resume carefully and extract only the
information that is actually present in the resume.

RESUME:
{resume_text}

Return ONLY valid JSON in exactly this structure:

{{
    "candidate_name": "",
    "professional_summary": "",
    "technical_skills": [],
    "tools_and_technologies": [],
    "soft_skills": [],
    "education": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "strengths": []
}}

Instructions:
1. Do not invent information.
2. Extract technical skills dynamically from the resume.
3. Extract tools, frameworks, libraries, and platforms.
4. Keep projects concise.
5. Extract education details if available.
6. Extract experience only if mentioned.
7. If a field is not available, return an empty list or empty string.
8. Return only valid JSON.
"""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise resume analysis system. "
                        "Always return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content

        resume_data = json.loads(response_text)

        return {
            "success": True,
            "data": resume_data,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }