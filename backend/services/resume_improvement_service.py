import json

from groq import Groq

from backend.config.settings import GROQ_API_KEY


def generate_resume_improvements(
    resume_data,
    job_data,
    career_match
):
    """
    Generates personalized resume improvement
    suggestions using the candidate's actual
    resume analysis and career match data.
    """

    try:

        # Create Groq AI client
        client = Groq(
            api_key=GROQ_API_KEY
        )

        # -----------------------------
        # EXTRACT RESUME INFORMATION
        # -----------------------------

        candidate_name = resume_data.get(
            "candidate_name",
            "Candidate"
        )

        professional_summary = resume_data.get(
            "professional_summary",
            ""
        )

        technical_skills = resume_data.get(
            "technical_skills",
            []
        )

        tools = resume_data.get(
            "tools_and_technologies",
            []
        )

        projects = resume_data.get(
            "projects",
            []
        )

        certifications = resume_data.get(
            "certifications",
            []
        )

        experience = resume_data.get(
            "experience",
            []
        )

        education = resume_data.get(
            "education",
            []
        )

        # -----------------------------
        # EXTRACT JOB INFORMATION
        # -----------------------------

        target_role = job_data.get(
            "job_title",
            "Not Specified"
        )

        job_keywords = job_data.get(
            "important_keywords",
            []
        )

        # -----------------------------
        # EXTRACT MATCH INFORMATION
        # -----------------------------

        current_score = career_match.get(
            "overall_score",
            0
        )

        skill_gap = career_match.get(
            "skill_gap_level",
            "Not Available"
        )

        missing_skills = career_match.get(
            "missing_skills",
            []
        )

        matching_skills = career_match.get(
            "matching_skills",
            []
        )

        recommendations = career_match.get(
            "recommendations",
            []
        )

        # -----------------------------
        # CREATE AI PROMPT
        # -----------------------------

        prompt = f"""
You are CareerForge AI, an expert AI resume
improvement and career optimization assistant.

Analyze the candidate's current resume information
against the target job role and provide personalized,
practical resume improvement suggestions.

CANDIDATE NAME:
{candidate_name}

TARGET JOB ROLE:
{target_role}

CURRENT CAREER MATCH SCORE:
{current_score}%

SKILL GAP LEVEL:
{skill_gap}

PROFESSIONAL SUMMARY:
{professional_summary}

TECHNICAL SKILLS:
{technical_skills}

TOOLS AND TECHNOLOGIES:
{tools}

PROJECTS:
{projects}

EXPERIENCE:
{experience}

CERTIFICATIONS:
{certifications}

EDUCATION:
{education}

MATCHING SKILLS:
{matching_skills}

MISSING SKILLS:
{missing_skills}

IMPORTANT JOB KEYWORDS:
{job_keywords}

CURRENT CAREER RECOMMENDATIONS:
{recommendations}

Return ONLY valid JSON in exactly this structure:

{{
    "overall_assessment": "",
    "professional_summary_improvement": "",
    "technical_skills_improvement": "",
    "projects_improvement": "",
    "keyword_optimization": [],
    "ats_suggestions": [],
    "priority_actions": [],
    "strengths_to_highlight": [],
    "final_resume_tip": ""
}}

Instructions:

1. Analyze only the data provided.
2. Do not claim that the candidate has skills
   that are not present in the resume.
3. Do not tell the candidate to falsely add
   missing skills to the resume.
4. For missing skills, suggest learning them
   and adding them only after gaining genuine
   knowledge or project experience.
5. Provide personalized and practical suggestions.
6. Suggest relevant keywords naturally based on
   the target role.
7. Prioritize the most important improvements.
8. Give ATS-friendly formatting suggestions.
9. Highlight existing strengths that should be
   emphasized.
10. Keep suggestions clear and concise.
11. Return ONLY valid JSON.
"""

        # -----------------------------
        # CALL GROQ AI
        # -----------------------------

        completion = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a precise AI resume improvement "
                        "system. Always return valid JSON only."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.3,

            response_format={
                "type": "json_object"
            }
        )

        # -----------------------------
        # PARSE AI RESPONSE
        # -----------------------------

        response_text = (
            completion
            .choices[0]
            .message
            .content
        )

        improvement_data = json.loads(
            response_text
        )

        return {

            "success": True,

            "data": improvement_data,

            "error": None

        }

    except Exception as e:

        return {

            "success": False,

            "data": None,

            "error": str(e)

        }