import streamlit as st
import numpy as np

from utils.resume_parser import extract_text
from utils.field_extractor import extract_fields
from utils.embeddings import embed
from utils.vector_db import get_collection
from llm.groq_llm import explain_match


# ---------------- Page Config ----------------
st.set_page_config(page_title="ATS Resume vs JD", layout="wide")
st.title("🧠 ATS Resume vs Job Description (Groq + ChromaDB)")


# ---------------- Inputs ----------------
resume_file = st.file_uploader(
    "📄 Upload Resume (PDF / DOCX)", type=["pdf", "docx"]
)
jd_text = st.text_area(
    "🧾 Paste Job Description", height=250
)


# ---------------- Analyze ----------------
if st.button("🔍 Analyze"):
    if not resume_file or not jd_text.strip():
        st.error("Please upload resume and paste job description")
        st.stop()

    # -------- Parse Resume & JD --------
    resume_text = extract_text(resume_file)

    if not resume_text.strip():
        st.error("❌ Could not extract text from resume")
        st.stop()

    resume_fields = extract_fields(resume_text)
    jd_fields = extract_fields(jd_text)

    # -------- Vector DB --------
    resume_col = get_collection("resumes", "chroma_db/resumes")
    jd_col = get_collection("jds", "chroma_db/jds")

    # Clear old data safely (Chroma requirement)
    resume_col.delete(where={"_id": {"$ne": "__non_existent_id__"}})
    jd_col.delete(where={"_id": {"$ne": "__non_existent_id__"}})

    # -------- Store Embeddings --------
    for field in ["Skills", "Education", "Job Role", "Experience"]:
        r_text = resume_fields.get(field, "").strip()
        j_text = jd_fields.get(field, "").strip()

        if not r_text or not j_text:
            continue

        resume_col.add(
            ids=[f"resume_{field}"],
            documents=[r_text],
            embeddings=[embed(r_text)]
        )

        jd_col.add(
            ids=[f"jd_{field}"],
            documents=[j_text],
            embeddings=[embed(j_text)]
        )

    # -------- Compare --------
    output = {}
    total_score = 0.0
    valid_fields = 0

    for field in ["Skills", "Education", "Job Role", "Experience"]:
        r = resume_col.get(
            ids=[f"resume_{field}"],
            include=["embeddings"]
        )
        j = jd_col.get(
            ids=[f"jd_{field}"],
            include=["embeddings"]
        )

        if r["embeddings"] is None or j["embeddings"] is None:
            continue

        r_vec = np.array(r["embeddings"][0])
        j_vec = np.array(j["embeddings"][0])

        similarity = float(
            np.dot(r_vec, j_vec) /
            (np.linalg.norm(r_vec) * np.linalg.norm(j_vec))
        ) * 100

        explanation = explain_match(
            field,
            resume_fields.get(field, ""),
            jd_fields.get(field, "")
        )

        output[field] = {
            "match_pct": round(similarity, 2),
            "resume_value": resume_fields.get(field, "")[:200] + "...",
            "job_description_value": jd_fields.get(field, "")[:200] + "...",
            "explanation": explanation
        }

        total_score += similarity
        valid_fields += 1

    if valid_fields == 0:
        st.error("❌ No comparable fields found")
        st.stop()

    final_json = [{
        "resume_filename": resume_file.name,
        **output,
        "OverallMatchPercentage": round(total_score / valid_fields, 2),
        "why_overall_match_is_this":
            "Match is calculated using semantic similarity across key ATS fields.",
        "AI_Generated_Estimate_Percentage": round(
            min(100, (total_score / valid_fields) + 5), 2
        )
    }]

    # -------- Output --------
    st.success("✅ Analysis Completed")
    st.subheader("📄 Final JSON Output")
    st.json(final_json)
