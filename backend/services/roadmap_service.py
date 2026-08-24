import json

from groq import Groq

from backend.config.settings import GROQ_API_KEY


def generate_learning_roadmap(
    resume_data,
    job_data,
    career_match
):
    """
    Generates a personalized learning roadmap
    based on the user's current skills, missing
    skills, target role, and career match.
    """

    try:

        # Create Groq AI client
        client = Groq(
            api_key=GROQ_API_KEY
        )


        # -----------------------------
        # EXTRACT USER DATA
        # -----------------------------

        target_role = job_data.get(
            "job_title",
            "Not specified"
        )

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

        technical_skills = resume_data.get(
            "technical_skills",
            []
        )

        tools = resume_data.get(
            "tools_and_technologies",
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
You are CareerForge AI, an expert AI career
learning path planner.

Create a personalized learning roadmap for the
candidate using their actual career analysis.

TARGET ROLE:
{target_role}

CURRENT CAREER MATCH SCORE:
{current_score}%

SKILL GAP LEVEL:
{skill_gap}

CURRENT TECHNICAL SKILLS:
{technical_skills}

CURRENT TOOLS AND TECHNOLOGIES:
{tools}

MATCHING SKILLS:
{matching_skills}

MISSING SKILLS:
{missing_skills}

CAREER RECOMMENDATIONS:
{recommendations}

Return ONLY valid JSON in exactly this format:

{{
    "target_role": "",
    "current_score": 0,
    "estimated_duration": "",
    "roadmap": [
        {{
            "phase": "Phase 1",
            "title": "",
            "skills": [],
            "duration": "",
            "description": "",
            "outcome": ""
        }}
    ],
    "final_project_suggestion": "",
    "career_tip": ""
}}

Instructions:

1. Generate a roadmap based on the candidate's
   actual missing skills and target role.

2. Do not provide a generic roadmap.

3. Prioritize the most important missing skills.

4. Organize the roadmap into logical learning phases.

5. Each phase should contain relevant skills.

6. Keep the roadmap realistic and beginner-friendly.

7. Mention an estimated duration for every phase.

8. Suggest one relevant final project.

9. Provide one short career tip.

10. Return ONLY valid JSON.
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
                        "You are a precise AI learning roadmap "
                        "generation system. Always return valid "
                        "JSON only."
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
        # PARSE RESPONSE
        # -----------------------------

        response_text = (
            completion
            .choices[0]
            .message
            .content
        )

        roadmap_data = json.loads(
            response_text
        )


        # -----------------------------
        # RETURN SUCCESS
        # -----------------------------

        return {

            "success": True,

            "data": roadmap_data,

            "error": None

        }


    # -----------------------------
    # HANDLE ERRORS
    # -----------------------------

    except Exception as e:

        return {

            "success": False,

            "data": None,

            "error": str(e)

        }