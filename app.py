import streamlit as st

from backend.services.resume_service import extract_resume_text
from backend.services.job_service import analyze_job
from backend.engines.resume_analyzer import analyze_resume
from backend.engines.match_engine import calculate_career_match
from backend.engines.skill_simulator import simulate_skill_impact
from backend.services.career_assistant import ask_career_question
from backend.services.roadmap_service import generate_learning_roadmap
from backend.services.resume_improvement_service import generate_resume_improvements


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CareerForge AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def render_tags(items, limit=None, empty_message="No information available."):
    """Display lists as compact horizontal skill tags."""
    clean_items = [str(item).strip() for item in (items or []) if str(item).strip()]

    if not clean_items:
        st.caption(empty_message)
        return

    shown_items = clean_items[:limit] if limit else clean_items

    tags_html = "".join(
        f'<span class="skill-tag">{item}</span>'
        for item in shown_items
    )

    st.markdown(
        f'<div class="tags-wrap">{tags_html}</div>',
        unsafe_allow_html=True
    )

    if limit and len(clean_items) > limit:
        st.caption(f"+ {len(clean_items) - limit} more")


def section_header(icon, title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-title">{icon} {title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def compact_list(items, label="", limit=12):
    if label:
        st.markdown(f"**{label}**")
    render_tags(items, limit=limit)


# ==================================================
# CUSTOM UI
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 5% 5%, rgba(247, 201, 229, 0.38), transparent 22%),
            radial-gradient(circle at 95% 10%, rgba(205, 220, 255, 0.45), transparent 24%),
            linear-gradient(180deg, #fff9fc 0%, #f7f8ff 45%, #ffffff 100%);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff7fb 0%, #f4f4ff 100%);
        border-right: 1px solid #e9dce8;
    }

    .hero {
        padding: 2.2rem 2rem;
        border-radius: 26px;
        background: linear-gradient(135deg, #fff1f7 0%, #f0f1ff 50%, #eef9ff 100%);
        border: 1px solid #eadced;
        box-shadow: 0 12px 34px rgba(104, 78, 120, 0.10);
        margin-bottom: 1.5rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.75);
        color: #7d5a82;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid #ead8e8;
    }

    .hero-title {
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.1;
        color: #3f3142;
        margin: 0.7rem 0 0.4rem 0;
    }

    .hero-title span { color: #b56c98; }

    .hero-text {
        font-size: 1.08rem;
        color: #716b78;
        max-width: 760px;
        line-height: 1.65;
    }

    .section-header {
        margin: 1.4rem 0 0.9rem 0;
        padding-left: 0.85rem;
        border-left: 4px solid #d99aba;
    }

    .section-title {
        font-size: 1.55rem;
        font-weight: 750;
        color: #443846;
    }

    .section-subtitle {
        color: #807887;
        margin-top: 0.2rem;
        font-size: 0.96rem;
    }

    .soft-card {
        background: rgba(255,255,255,0.78);
        border: 1px solid #eee5ed;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 5px 16px rgba(70, 50, 80, 0.04);
        margin-bottom: 0.8rem;
    }

    .tags-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.4rem 0 0.8rem 0;
    }

    .skill-tag {
        display: inline-flex;
        align-items: center;
        padding: 0.34rem 0.72rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #fff1f7, #f3f1ff);
        border: 1px solid #eadde9;
        color: #645464;
        font-size: 0.86rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .step-item {
        padding: 0.55rem 0.65rem;
        border-radius: 12px;
        margin: 0.35rem 0;
        color: #655968;
        font-size: 0.9rem;
    }

    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid #d9b8cb !important;
        background: linear-gradient(135deg, #d994ba, #b9a2d8) !important;
        color: white !important;
        font-weight: 700 !important;
        min-height: 2.8rem;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(180, 112, 153, 0.22);
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.82);
        border: 1px solid #ece3eb;
        border-radius: 16px;
        padding: 0.9rem;
        box-shadow: 0 5px 14px rgba(60,40,70,0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #7c7180;
    }

    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.75);
        border: 1px solid #eee5ed;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 0.65rem;
    }

    .footer {
        text-align: center;
        color: #8d8490;
        font-size: 0.88rem;
        padding: 2rem 0 0.5rem;
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #e5d9e4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("## ✨ CareerForge AI")
    st.caption("Your friendly AI career companion")
    st.divider()

    st.markdown("### 🧭 Your workflow")

    steps = [
        "1. 📄 Upload your resume",
        "2. 🎯 Analyze your target role",
        "3. 🤖 Understand your profile",
        "4. 📊 Check your career match",
        "5. 🔮 Simulate a new skill",
        "6. 💬 Ask CareerForge AI",
        "7. 🗺️ Build your roadmap",
        "8. ✨ Improve your resume",
    ]

    for step in steps:
        st.markdown(f'<div class="step-item">{step}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💡 Quick tip")
    st.caption(
        "Start with a job title and your resume. The remaining tools will personalize their results based on your analysis."
    )

    if st.button("🧹 Start Fresh", use_container_width=True, key="clear_app"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✦ AI-POWERED CAREER INTELLIGENCE</div>
        <div class="hero-title">Build your next career move with <span>clarity.</span></div>
        <div class="hero-text">
            Upload your resume, explore a target role, discover skill gaps, simulate career growth,
            and get personalized guidance — all in one friendly workspace.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 1. RESUME UPLOAD
# ==================================================

section_header(
    "📄",
    "Upload your resume",
    "Start by uploading your PDF resume. We will use it to personalize the complete career analysis."
)

uploaded_file = st.file_uploader(
    "Choose your Resume PDF",
    type=["pdf"],
    help="Please upload your resume in PDF format."
)

if uploaded_file is not None:
    file_signature = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.get("uploaded_file_signature") != file_signature:
        with st.spinner("Extracting resume information..."):
            result = extract_resume_text(uploaded_file)

        if result.get("success"):
            st.session_state["resume_text"] = result.get("text", "")
            st.session_state["uploaded_file_signature"] = file_signature
            st.session_state["resume_page_count"] = result.get("page_count", 0)
            st.success(f"Resume ready ✨ {uploaded_file.name}")
        else:
            st.error(f"Error while reading the resume: {result.get('error', 'Unknown error')}")

    if "resume_text" in st.session_state:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.caption("Your resume text was extracted successfully and is ready for AI analysis.")
        with c2:
            st.metric("Pages", st.session_state.get("resume_page_count", 0))

        with st.expander("👀 Preview extracted resume text"):
            st.text_area(
                "Resume Preview",
                value=st.session_state["resume_text"][:5000],
                height=300,
                key="resume_preview"
            )
else:
    st.info("Upload a PDF resume to unlock the personalized analysis.")


# ==================================================
# 2. JOB ANALYSIS
# ==================================================

section_header(
    "🎯",
    "Tell us about your target role",
    "Enter a job title, paste a job description, or provide both."
)

job_title = st.text_input(
    "Target Job Title",
    placeholder="Example: AI/ML Engineer",
    key="job_title_input"
)

job_description = st.text_area(
    "Job Description (optional)",
    placeholder="Paste the job description here. CareerForge AI will extract role-specific requirements...",
    height=180,
    key="job_description_input"
)

if st.button("🔍 Analyze Job Requirements", use_container_width=True, key="analyze_job_button"):
    if not job_title.strip() and not job_description.strip():
        st.warning("Please enter a job title or job description.")
    else:
        with st.spinner("AI is analyzing the role requirements..."):
            job_result = analyze_job(job_title=job_title, job_description=job_description)

        if job_result.get("success"):
            st.session_state["job_analysis"] = job_result.get("data", {})
            for key in ["career_match", "skill_simulation", "career_assistant_answer", "learning_roadmap", "resume_improvements"]:
                st.session_state.pop(key, None)
            st.success("Job requirements analyzed successfully!")
        else:
            st.error(f"Job analysis failed: {job_result.get('error', 'Unknown error')}")

if "job_analysis" in st.session_state:
    job_data = st.session_state["job_analysis"]

    with st.expander("✨ View Job Analysis Summary", expanded=True):
        st.markdown(f"### 🎯 {job_data.get('job_title', 'Target Role')}")

        c1, c2 = st.columns(2)
        with c1:
            compact_list(job_data.get("technical_skills", []), "💻 Technical skills")
            compact_list(job_data.get("tools_and_technologies", []), "🛠️ Tools & technologies")
        with c2:
            compact_list(job_data.get("soft_skills", []), "🤝 Soft skills")
            st.markdown("**🎓 Experience**")
            st.caption(
                f"{job_data.get('experience_level', 'Not specified')} • "
                f"{job_data.get('experience_required', 'Not specified')}"
            )

        responsibilities = job_data.get("responsibilities", [])
        keywords = job_data.get("important_keywords", [])

        if responsibilities or keywords:
            with st.expander("📌 Responsibilities & important keywords"):
                if responsibilities:
                    st.markdown("**Main responsibilities**")
                    for responsibility in responsibilities[:8]:
                        st.write(f"• {responsibility}")
                compact_list(keywords, "🔑 Important keywords", limit=18)


# ==================================================
# 3. AI RESUME ANALYSIS
# ==================================================

if "resume_text" in st.session_state:
    section_header(
        "🤖",
        "AI Resume Analysis",
        "Let CareerForge AI turn your resume into a clear professional profile."
    )

    if st.button("🤖 Analyze My Resume", use_container_width=True, key="analyze_resume_button"):
        with st.spinner("CareerForge AI is reading your professional profile..."):
            resume_result = analyze_resume(st.session_state["resume_text"])

        if resume_result.get("success"):
            st.session_state["resume_analysis"] = resume_result.get("data", {})
            for key in ["career_match", "skill_simulation", "career_assistant_answer", "learning_roadmap", "resume_improvements"]:
                st.session_state.pop(key, None)
            st.success("Resume analyzed successfully!")
        else:
            st.error(f"Resume analysis failed: {resume_result.get('error', 'Unknown error')}")

if "resume_analysis" in st.session_state:
    resume_data = st.session_state["resume_analysis"]

    with st.expander("👤 View My AI Resume Profile", expanded=True):
        candidate_name = resume_data.get("candidate_name", "Candidate")
        st.markdown(f"### 👋 {candidate_name}")

        summary = resume_data.get("professional_summary", "")
        if summary:
            st.caption(summary)

        c1, c2 = st.columns(2)
        with c1:
            compact_list(resume_data.get("technical_skills", []), "💻 Technical skills")
            compact_list(resume_data.get("tools_and_technologies", []), "🛠️ Tools & technologies")
        with c2:
            compact_list(resume_data.get("soft_skills", []), "🤝 Soft skills")
            compact_list(resume_data.get("certifications", []), "🏆 Certifications")

        with st.expander("🎓 Education, experience & projects"):
            for title, key in [
                ("🎓 Education", "education"),
                ("💼 Experience", "experience"),
                ("🚀 Projects", "projects"),
                ("✨ Strengths", "strengths"),
            ]:
                values = resume_data.get(key, [])
                if values:
                    st.markdown(f"**{title}**")
                    for value in values:
                        st.write(f"• {value}")


# ==================================================
# 4. CAREER MATCH
# ==================================================

if "resume_analysis" in st.session_state and "job_analysis" in st.session_state:
    section_header(
        "📊",
        "Career Match Analysis",
        "Compare your current profile with the target role and discover where you stand."
    )

    if st.button("🚀 Calculate My Career Match", use_container_width=True, key="calculate_match_button"):
        with st.spinner("Comparing your profile with the target role..."):
            match_result = calculate_career_match(
                resume_data=st.session_state["resume_analysis"],
                job_data=st.session_state["job_analysis"]
            )

        if isinstance(match_result, dict):
            st.session_state["career_match"] = match_result
            for key in ["skill_simulation", "career_assistant_answer", "learning_roadmap", "resume_improvements"]:
                st.session_state.pop(key, None)
            st.success("Your career match report is ready!")
        else:
            st.error("Career match calculation did not return valid data.")

if "career_match" in st.session_state:
    match_data = st.session_state["career_match"]
    overall_score = float(match_data.get("overall_score", 0) or 0)

    section_header("🌟", "Your Career Match Report", "A compact view of your alignment, strengths, gaps and next actions.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Overall Match", f"{overall_score:.0f}%")
    with c2:
        st.metric("Skill Gap", match_data.get("skill_gap_level", "Not Available"))
    with c3:
        st.metric("Missing Skills", len(match_data.get("missing_skills", []) or []))

    st.progress(max(0, min(int(overall_score), 100)))

    if overall_score >= 80:
        st.success("🌿 Strong match — your profile is well aligned with this role.")
    elif overall_score >= 50:
        st.warning("🌼 Good foundation — improving a few high-impact skills could strengthen your match.")
    else:
        st.info("🌱 Growth opportunity — use the missing skills and recommendations to build a stronger profile.")

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("✅ Matching skills", expanded=True):
            render_tags(match_data.get("matching_skills", []), limit=24, empty_message="No matching skills identified.")
    with c2:
        with st.expander("🌱 Skills to develop", expanded=True):
            render_tags(match_data.get("missing_skills", []), limit=24, empty_message="No major skills are missing!")

    with st.expander("📈 Score breakdown"):
        breakdown = match_data.get("score_breakdown", {}) or {}
        labels = [
            ("💻 Technical Skills", "technical_skills"),
            ("🛠️ Tools & Technologies", "tools_and_technologies"),
            ("🤝 Soft Skills", "soft_skills"),
            ("🔑 Important Keywords", "important_keywords"),
        ]
        for label, key in labels:
            score = float(breakdown.get(key, 0) or 0)
            st.write(f"**{label}: {score:.0f}%**")
            st.progress(max(0, min(int(score), 100)))

    with st.expander("🔍 Detailed skill analysis"):
        for title, key in [
            ("💻 Technical Skills", "technical_skills"),
            ("🛠️ Tools & Technologies", "tools_and_technologies"),
        ]:
            data = match_data.get(key, {}) or {}
            st.markdown(f"**{title} • {data.get('score', 0)}% match**")
            compact_list(data.get("matching", []), "Matching")
            compact_list(data.get("missing", []), "Missing")

    recommendations = match_data.get("recommendations", [])
    if recommendations:
        with st.expander("💡 Personalized recommendations"):
            for index, recommendation in enumerate(recommendations, start=1):
                st.write(f"{index}. {recommendation}")


# ==================================================
# 5. WHAT-IF SKILL SIMULATOR
# ==================================================

if all(key in st.session_state for key in ["career_match", "resume_analysis", "job_analysis"]):
    section_header(
        "🔮",
        "What if I learned this skill?",
        "Choose a missing skill and simulate its possible impact before adding it to your real profile."
    )

    missing_skills = st.session_state["career_match"].get("missing_skills", []) or []

    if missing_skills:
        selected_skill = st.selectbox(
            "Choose a skill to simulate",
            options=missing_skills,
            key="skill_simulator_select"
        )

        if st.button("🔮 Simulate Skill Impact", use_container_width=True, key="simulate_skill_button"):
            with st.spinner("Calculating the possible impact..."):
                simulation_result = simulate_skill_impact(
                    resume_data=st.session_state["resume_analysis"],
                    job_data=st.session_state["job_analysis"],
                    current_match=st.session_state["career_match"],
                    selected_skill=selected_skill
                )
            st.session_state["skill_simulation"] = simulation_result
    else:
        st.info("No missing skills are currently available for simulation.")

if "skill_simulation" in st.session_state:
    simulation = st.session_state["skill_simulation"]
    if simulation.get("success"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Current Score", f"{simulation.get('current_score', 0)}%")
        with c2:
            st.metric("New Score", f"{simulation.get('new_score', 0)}%")
        with c3:
            improvement = simulation.get("improvement", 0)
            sign = "+" if improvement >= 0 else ""
            st.metric("Possible Improvement", f"{sign}{improvement}%")

        st.success(
            f"✨ Learning **{simulation.get('selected_skill', '')}** could change your estimated career match from "
            f"**{simulation.get('current_score', 0)}%** to **{simulation.get('new_score', 0)}%**."
        )
    else:
        st.error(simulation.get("error", "Simulation failed."))


# ==================================================
# 6. AI CAREER ASSISTANT
# ==================================================

if all(key in st.session_state for key in ["resume_analysis", "job_analysis", "career_match"]):
    section_header(
        "💬",
        "Ask CareerForge AI",
        "Ask anything about your resume, skills, career match, missing skills or next steps."
    )

    career_question = st.text_area(
        "What would you like to know?",
        placeholder="Example: Which skill should I learn first to improve my career match?",
        height=110,
        key="career_question_input"
    )

    if st.button("🤖 Ask CareerForge AI", use_container_width=True, key="ask_career_button"):
        if not career_question.strip():
            st.warning("Please enter your career question.")
        else:
            with st.spinner("CareerForge AI is thinking..."):
                career_response = ask_career_question(
                    question=career_question,
                    resume_data=st.session_state["resume_analysis"],
                    job_data=st.session_state["job_analysis"],
                    career_match=st.session_state["career_match"]
                )

            if career_response.get("success"):
                st.session_state["career_assistant_answer"] = career_response.get("answer", "")
            else:
                st.error(career_response.get("error", "Unable to generate a response."))

if "career_assistant_answer" in st.session_state:
    with st.expander("🤖 CareerForge AI's answer", expanded=True):
        st.markdown(st.session_state["career_assistant_answer"])


# ==================================================
# 7. LEARNING ROADMAP
# ==================================================

if all(key in st.session_state for key in ["resume_analysis", "job_analysis", "career_match"]):
    section_header(
        "🗺️",
        "Personalized Learning Roadmap",
        "Turn your skill gaps into a practical learning journey designed for your target role."
    )

    if st.button("🗺️ Generate My Learning Roadmap", use_container_width=True, key="generate_roadmap_button"):
        with st.spinner("Creating your personalized learning roadmap..."):
            roadmap_result = generate_learning_roadmap(
                resume_data=st.session_state["resume_analysis"],
                job_data=st.session_state["job_analysis"],
                career_match=st.session_state["career_match"]
            )

        if roadmap_result.get("success"):
            st.session_state["learning_roadmap"] = roadmap_result.get("data", {})
        else:
            st.error(roadmap_result.get("error", "Unable to generate learning roadmap."))

if "learning_roadmap" in st.session_state:
    roadmap_data = st.session_state["learning_roadmap"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Target Role", roadmap_data.get("target_role", "Not Specified"))
    with c2:
        st.metric("Current Score", f"{roadmap_data.get('current_score', 0)}%")
    with c3:
        st.metric("Estimated Duration", roadmap_data.get("estimated_duration", "Not Specified"))

    roadmap = roadmap_data.get("roadmap", []) or []
    if roadmap:
        for step in roadmap:
            phase = step.get("phase", "Learning Phase")
            title = step.get("title", "")
            skills = step.get("skills", [])
            duration = step.get("duration", "Not Specified")
            description = step.get("description", "")
            outcome = step.get("outcome", "")

            with st.expander(f"{phase}: {title}"):
                st.caption(f"⏱️ {duration}")
                compact_list(skills, "📚 Skills to learn")
                if description:
                    st.write(f"**What to do:** {description}")
                if outcome:
                    st.success(f"🎯 Outcome: {outcome}")
    else:
        st.warning("No roadmap phases were generated.")

    c1, c2 = st.columns(2)
    with c1:
        final_project = roadmap_data.get("final_project_suggestion", "")
        if final_project:
            with st.expander("🚀 Recommended final project"):
                st.write(final_project)
    with c2:
        career_tip = roadmap_data.get("career_tip", "")
        if career_tip:
            with st.expander("💡 Career tip"):
                st.write(career_tip)


# ==================================================
# 8. RESUME IMPROVEMENTS
# ==================================================

if all(key in st.session_state for key in ["resume_analysis", "job_analysis", "career_match"]):
    section_header(
        "✨",
        "Resume Improvement Suggestions",
        "Get personalized ideas to improve your resume for the role you want."
    )

    if st.button("✨ Analyze How I Can Improve My Resume", use_container_width=True, key="generate_improvement_button"):
        with st.spinner("CareerForge AI is preparing your improvement report..."):
            improvement_result = generate_resume_improvements(
                resume_data=st.session_state["resume_analysis"],
                job_data=st.session_state["job_analysis"],
                career_match=st.session_state["career_match"]
            )

        if improvement_result.get("success"):
            st.session_state["resume_improvements"] = improvement_result.get("data", {})
        else:
            st.error(improvement_result.get("error", "Unable to generate resume improvements."))

if "resume_improvements" in st.session_state:
    improvement_data = st.session_state["resume_improvements"]

    overall_assessment = improvement_data.get("overall_assessment", "")
    if overall_assessment:
        st.info(overall_assessment)

    improvement_sections = [
        ("📝 Improve Your Professional Summary", "professional_summary_improvement"),
        ("💻 Improve Your Technical Skills Section", "technical_skills_improvement"),
        ("🚀 Improve Your Projects Section", "projects_improvement"),
    ]

    for title, key in improvement_sections:
        value = improvement_data.get(key, "")
        if value:
            with st.expander(title):
                st.write(value)

    keyword_optimization = improvement_data.get("keyword_optimization", [])
    ats_suggestions = improvement_data.get("ats_suggestions", [])
    priority_actions = improvement_data.get("priority_actions", [])
    strengths = improvement_data.get("strengths_to_highlight", [])

    c1, c2 = st.columns(2)
    with c1:
        with st.expander("🔑 Keyword optimization"):
            render_tags(keyword_optimization, limit=24)
        with st.expander("✨ Strengths to highlight"):
            render_tags(strengths, limit=24)
    with c2:
        with st.expander("🤖 ATS-friendly suggestions"):
            for suggestion in ats_suggestions:
                st.write(f"• {suggestion}")
        with st.expander("🔥 Priority action plan"):
            for index, action in enumerate(priority_actions, start=1):
                st.write(f"{index}. {action}")

    final_tip = improvement_data.get("final_resume_tip", "")
    if final_tip:
        st.success(f"💡 Final tip: {final_tip}")


# ==================================================
# FOOTER
# ==================================================

st.divider()
st.markdown(
    """
    <div class="footer">
        <b>CareerForge AI</b><br>
        Resume intelligence • Career matching • Skill growth • Personalized guidance<br><br>
        Built  By Gaikwad Mayuri  ✨
    </div>
    """,
    unsafe_allow_html=True
)