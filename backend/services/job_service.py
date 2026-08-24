import json
from groq import Groq

from backend.config.settings import GROQ_API_KEY


def analyze_job(job_title="", job_description=""):
    """
    Analyzes a job title and/or job description dynamically
    using Groq AI.
    """

    if not job_title.strip() and not job_description.strip():
        return {
            "success": False,
            "data": None,
            "error": "Please provide a job title or job description."
        }

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an expert AI recruitment and career analysis system.

Analyze the following job information:

JOB TITLE:
{job_title}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON in the following format:

{{
    "job_title": "identified job title",
    "technical_skills": [],
    "tools_and_technologies": [],
    "soft_skills": [],
    "experience_level": "Fresher/Junior/Mid/Senior/Not specified",
    "experience_required": "experience requirement",
    "education_requirements": [],
    "responsibilities": [],
    "important_keywords": []
}}

Instructions:
1. Extract skills dynamically from the provided job information.
2. Do not use hardcoded skills.
3. If only a job title is provided, infer common requirements for that role.
4. If a job description is provided, prioritize the exact requirements in it.
5. Return only JSON without markdown formatting or explanations.
"""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise job requirement extraction system. "
                        "Always return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content

        job_data = json.loads(response_text)

        return {
            "success": True,
            "data": job_data,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }