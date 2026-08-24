import copy

from backend.engines.match_engine import calculate_career_match


def normalize_skill(skill):
    """
    Converts a skill into a clean format
    for comparison.
    """

    if not isinstance(skill, str):
        return ""

    return skill.strip().lower()


def skill_exists_in_list(skill, items):
    """
    Checks whether a skill already exists
    in a list, ignoring case.
    """

    normalized_skill = normalize_skill(skill)

    for item in items:

        if normalize_skill(item) == normalized_skill:
            return True

    return False


def add_skill_to_category(
    resume_data,
    category,
    selected_skill
):
    """
    Adds the selected skill to a specific
    resume category only if it does not
    already exist.
    """

    current_items = resume_data.get(
        category,
        []
    )

    # Ensure the value is a list
    if not isinstance(current_items, list):

        current_items = []

    # Add skill only if it does not exist
    if not skill_exists_in_list(
        selected_skill,
        current_items
    ):

        current_items.append(selected_skill)

    # Save updated category
    resume_data[category] = current_items


def simulate_skill_impact(
    resume_data,
    job_data,
    current_match,
    selected_skill
):
    """
    Simulates the impact of learning one
    missing skill.

    The original resume data is not modified.

    The selected skill is temporarily added
    to the correct category based on the
    job requirements and the career match
    score is recalculated.
    """

    # --------------------------------
    # VALIDATE SELECTED SKILL
    # --------------------------------

    if not isinstance(selected_skill, str):

        return {
            "success": False,
            "error": "Please select a valid skill."
        }

    selected_skill = selected_skill.strip()

    if not selected_skill:

        return {
            "success": False,
            "error": "Please select a valid skill."
        }

    # --------------------------------
    # CREATE TEMPORARY COPY
    # --------------------------------

    # Original resume data remains unchanged
    simulated_resume = copy.deepcopy(
        resume_data
    )

    normalized_selected_skill = normalize_skill(
        selected_skill
    )

    # --------------------------------
    # GET JOB REQUIREMENT CATEGORIES
    # --------------------------------

    job_technical_skills = job_data.get(
        "technical_skills",
        []
    )

    job_tools = job_data.get(
        "tools_and_technologies",
        []
    )

    job_soft_skills = job_data.get(
        "soft_skills",
        []
    )

    job_keywords = job_data.get(
        "important_keywords",
        []
    )

    # --------------------------------
    # CHECK WHERE THE SKILL BELONGS
    # --------------------------------

    skill_added = False
    added_categories = []

    # TECHNICAL SKILLS

    if skill_exists_in_list(
        selected_skill,
        job_technical_skills
    ):

        add_skill_to_category(
            simulated_resume,
            "technical_skills",
            selected_skill
        )

        skill_added = True

        added_categories.append(
            "technical skills"
        )

    # TOOLS & TECHNOLOGIES

    if skill_exists_in_list(
        selected_skill,
        job_tools
    ):

        add_skill_to_category(
            simulated_resume,
            "tools_and_technologies",
            selected_skill
        )

        skill_added = True

        added_categories.append(
            "tools and technologies"
        )

    # SOFT SKILLS

    if skill_exists_in_list(
        selected_skill,
        job_soft_skills
    ):

        add_skill_to_category(
            simulated_resume,
            "soft_skills",
            selected_skill
        )

        skill_added = True

        added_categories.append(
            "soft skills"
        )

    # --------------------------------
    # KEYWORD ONLY CASE
    # --------------------------------

    # If the skill is present only in
    # important keywords, add it to
    # technical skills so it becomes
    # part of resume_all_skills in
    # match_engine.py.

    if (
        not skill_added
        and skill_exists_in_list(
            selected_skill,
            job_keywords
        )
    ):

        add_skill_to_category(
            simulated_resume,
            "technical_skills",
            selected_skill
        )

        skill_added = True

        added_categories.append(
            "important keywords"
        )

    # --------------------------------
    # SKILL NOT FOUND IN JOB
    # --------------------------------

    if not skill_added:

        return {
            "success": False,
            "error": (
                f"'{selected_skill}' was not found "
                "in the job requirements. Please select "
                "a skill from the missing skills list."
            )
        }

    # --------------------------------
    # RECALCULATE CAREER MATCH
    # --------------------------------

    simulated_match = calculate_career_match(
        resume_data=simulated_resume,
        job_data=job_data
    )

    # --------------------------------
    # GET SCORES
    # --------------------------------

    current_score = current_match.get(
        "overall_score",
        0
    )

    new_score = simulated_match.get(
        "overall_score",
        0
    )

    improvement = round(
        new_score - current_score,
        2
    )

    # --------------------------------
    # RETURN RESULT
    # --------------------------------

    return {
        "success": True,

        "selected_skill": selected_skill,

        "current_score": current_score,

        "new_score": new_score,

        "improvement": improvement,

        "added_categories": added_categories,

        "simulated_match": simulated_match
    }