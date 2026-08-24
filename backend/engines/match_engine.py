def normalize_text(value):
    """
    Converts text into a standard format
    for better comparison.
    """

    if not isinstance(value, str):
        return ""

    return value.strip().lower()


def get_normalized_list(items):
    """
    Converts a list of values into a cleaned
    and normalized set.
    """

    if not items:
        return set()

    normalized_items = set()

    for item in items:
        if isinstance(item, str):

            cleaned_item = normalize_text(item)

            if cleaned_item:
                normalized_items.add(cleaned_item)

    return normalized_items


def calculate_category_match(job_items, resume_items):
    """
    Compares one category of requirements.

    Example:
    Job skills: Python, SQL, Docker
    Resume skills: Python, SQL

    Returns:
    Match percentage, matching items, missing items
    """

    job_set = get_normalized_list(job_items)
    resume_set = get_normalized_list(resume_items)

    if not job_set:
        return {
            "score": 100.0,
            "matching": [],
            "missing": []
        }

    matching = job_set.intersection(resume_set)
    missing = job_set.difference(resume_set)

    score = (
        len(matching) / len(job_set)
    ) * 100

    return {
        "score": round(score, 2),
        "matching": sorted(list(matching)),
        "missing": sorted(list(missing))
    }


def calculate_career_match(resume_data, job_data):
    """
    Main CareerForge matching engine.

    Dynamically compares resume analysis
    with job analysis.
    """

    # -----------------------------
    # TECHNICAL SKILLS
    # -----------------------------

    technical_result = calculate_category_match(
        job_data.get("technical_skills", []),
        resume_data.get("technical_skills", [])
    )


    # -----------------------------
    # TOOLS & TECHNOLOGIES
    # -----------------------------

    tools_result = calculate_category_match(
        job_data.get("tools_and_technologies", []),
        resume_data.get("tools_and_technologies", [])
    )


    # -----------------------------
    # SOFT SKILLS
    # -----------------------------

    soft_skills_result = calculate_category_match(
        job_data.get("soft_skills", []),
        resume_data.get("soft_skills", [])
    )


    # -----------------------------
    # IMPORTANT KEYWORDS
    # -----------------------------

    resume_all_skills = (
        resume_data.get("technical_skills", [])
        + resume_data.get(
            "tools_and_technologies",
            []
        )
        + resume_data.get("soft_skills", [])
    )

    keyword_result = calculate_category_match(
        job_data.get("important_keywords", []),
        resume_all_skills
    )


    # -----------------------------
    # SCORE WEIGHTS
    # -----------------------------

    weights = {
        "technical_skills": 0.50,
        "tools": 0.25,
        "soft_skills": 0.10,
        "keywords": 0.15
    }


    overall_score = (
        technical_result["score"]
        * weights["technical_skills"]

        + tools_result["score"]
        * weights["tools"]

        + soft_skills_result["score"]
        * weights["soft_skills"]

        + keyword_result["score"]
        * weights["keywords"]
    )


    overall_score = round(overall_score, 2)


    # -----------------------------
    # COLLECT MATCHING SKILLS
    # -----------------------------

    matching_skills = sorted(
        set(
            technical_result["matching"]
            + tools_result["matching"]
            + soft_skills_result["matching"]
        )
    )


    # -----------------------------
    # COLLECT MISSING SKILLS
    # -----------------------------

    missing_skills = sorted(
        set(
            technical_result["missing"]
            + tools_result["missing"]
        )
    )


    # -----------------------------
    # DETERMINE SKILL GAP
    # -----------------------------

    if overall_score >= 80:

        skill_gap_level = "Low"

    elif overall_score >= 50:

        skill_gap_level = "Moderate"

    else:

        skill_gap_level = "High"


    # -----------------------------
    # GENERATE RECOMMENDATIONS
    # -----------------------------

    recommendations = []

    if technical_result["missing"]:

        recommendations.append(
            "Focus on learning the missing technical skills "
            "required for this role."
        )

    if tools_result["missing"]:

        recommendations.append(
            "Gain practical experience with the missing "
            "tools and technologies."
        )

    if overall_score < 50:

        recommendations.append(
            "Build role-specific projects to strengthen "
            "your profile."
        )

    elif overall_score < 80:

        recommendations.append(
            "Improve your profile by strengthening the "
            "highest-impact missing skills."
        )

    else:

        recommendations.append(
            "Your profile is strongly aligned with the "
            "selected job requirements."
        )


    # -----------------------------
    # FINAL RESULT
    # -----------------------------

    return {
        "overall_score": overall_score,

        "skill_gap_level": skill_gap_level,

        "technical_skills": technical_result,

        "tools_and_technologies": tools_result,

        "soft_skills": soft_skills_result,

        "important_keywords": keyword_result,

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "recommendations": recommendations,

        "score_breakdown": {
            "technical_skills": technical_result["score"],
            "tools_and_technologies": tools_result["score"],
            "soft_skills": soft_skills_result["score"],
            "important_keywords": keyword_result["score"]
        }
    }