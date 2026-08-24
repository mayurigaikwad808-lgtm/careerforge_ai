from groq import Groq

from backend.config.settings import GROQ_API_KEY


def ask_career_question(
    question,
    resume_data,
    job_data,
    career_match
):
    """
    Answers career-related questions using the
    user's actual resume analysis, job analysis,
    and career match data.
    """

    # --------------------------------
    # VALIDATE QUESTION
    # --------------------------------

    if not question or not question.strip():

        return {
            "success": False,
            "answer": None,
            "error": "Please enter a career-related question."
        }


    # --------------------------------
    # CREATE AI CLIENT
    # --------------------------------

    try:

        client = Groq(
            api_key=GROQ_API_KEY
        )


        # --------------------------------
        # EXTRACT IMPORTANT DATA
        # --------------------------------

        candidate_name = resume_data.get(
            "candidate_name",
            "Candidate"
        )

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
            "Not available"
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

        resume_skills = resume_data.get(
            "technical_skills",
            []
        )

        resume_tools = resume_data.get(
            "tools_and_technologies",
            []
        )

        projects = resume_data.get(
            "projects",
            []
        )


        # --------------------------------
        # BUILD DYNAMIC CONTEXT
        # --------------------------------

        prompt = f"""
You are CareerForge AI, an intelligent and supportive
AI career guidance assistant.

You must answer the user's question based on their
actual career analysis data provided below.

CANDIDATE INFORMATION:
Name: {candidate_name}

TARGET JOB ROLE:
{target_role}

CURRENT CAREER MATCH SCORE:
{current_score}%

SKILL GAP LEVEL:
{skill_gap}

MATCHING SKILLS:
{matching_skills}

MISSING SKILLS:
{missing_skills}

CANDIDATE TECHNICAL SKILLS:
{resume_skills}

CANDIDATE TOOLS AND TECHNOLOGIES:
{resume_tools}

CANDIDATE PROJECTS:
{projects}

CAREER RECOMMENDATIONS:
{recommendations}

USER QUESTION:
{question}

Instructions:

1. Give a personalized answer based on the provided data.
2. Do not pretend to know information not present in the analysis.
3. Prioritize the candidate's actual missing skills.
4. Give practical and actionable advice.
5. If the question is about score improvement, explain which
   missing skills could have the highest impact.
6. If the question is about projects, suggest projects relevant
   to the target role and skill gaps.
7. Keep the answer clear, supportive, and professional.
8. Use headings and bullet points when helpful.
9. Do not return JSON.
"""


        # --------------------------------
        # CALL GROQ AI
        # --------------------------------

        completion = (
            client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are CareerForge AI, a personalized "
                            "AI career guidance assistant. Provide "
                            "accurate, practical, and helpful career advice."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.4,

                max_completion_tokens=1000
            )
        )


        answer = (
            completion
            .choices[0]
            .message
            .content
        )


        # --------------------------------
        # RETURN SUCCESS
        # --------------------------------

        return {

            "success": True,

            "answer": answer,

            "error": None

        }


    # --------------------------------
    # HANDLE ERRORS
    # --------------------------------

    except Exception as e:

        return {

            "success": False,

            "answer": None,

            "error": str(e)

        }