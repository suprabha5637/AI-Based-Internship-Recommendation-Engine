import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI-Based Internship Recommendation Engine API",
    description="Intelligent Hybrid Recommendation Engine combining Jaccard Similarity, TF-IDF, and Rule-Based Matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load Internship Dataset ----------
# Resilient path resolution for running from root or app/
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "..", "internships.csv")
if not os.path.exists(csv_path):
    csv_path = os.path.join(os.getcwd(), "internships.csv")

df = pd.read_csv(csv_path)

# Fill NA values for standard columns
for col in ["skills", "category", "education", "job_loc", "job_title", "company_name", "compensation"]:
    if col in df.columns:
        df[col] = df[col].fillna("")

# ---------- Utility: Jaccard Similarity ----------
def jaccard_similarity(set1, set2):
    s1 = set([str(s).lower().strip() for s in set1 if str(s).strip()])
    s2 = set([str(s).lower().strip() for s in set2 if str(s).strip()])
    inter = len(s1 & s2)
    union = len(s1 | s2)
    return inter / union if union > 0 else 0

# ---------- Core Recommendation ----------
def recommend_internships(candidate: dict, top_n: int = 5):
    filtered = df.copy()

    # Rule-based soft matches
    filtered["sector_match"] = filtered["category"].str.contains(
        str(candidate.get("sector_interest", "")), case=False, na=False
    ).astype(int)

    filtered["location_match"] = filtered["job_loc"].str.contains(
        str(candidate.get("location_preference", "")), case=False, na=False
    ).astype(int)

    filtered["education_match"] = filtered["education"].str.contains(
        str(candidate.get("education", "")), case=False, na=False
    ).astype(int)

    # Jaccard skill similarity
    scores = []
    candidate_skills = candidate.get("skills", [])
    for _, row in filtered.iterrows():
        internship_skills = [s.strip() for s in str(row["skills"]).split(",") if s.strip()]
        score = jaccard_similarity(candidate_skills, internship_skills)
        scores.append(score)
    filtered["jaccard_score"] = scores

    # TF-IDF similarity
    filtered["combined_text"] = (
        filtered["skills"].fillna('') + " " +
        filtered["category"].fillna('') + " " +
        filtered["education"].fillna('') + " " +
        filtered["job_loc"].fillna('')
    )
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(filtered["combined_text"].values)

    candidate_text = (
        " ".join(candidate_skills) + " " +
        str(candidate.get("sector_interest", "")) + " " +
        str(candidate.get("location_preference", "")) + " " +
        str(candidate.get("education", ""))
    )
    candidate_vec = vectorizer.transform([candidate_text])
    tfidf_similarities = cosine_similarity(candidate_vec, tfidf_matrix).flatten()
    filtered["tfidf_score"] = tfidf_similarities

    # Hybrid Scoring
    filtered["final_score"] = (
        0.5 * filtered["jaccard_score"] +
        0.2 * filtered["sector_match"] +
        0.1 * filtered["location_match"] +
        0.1 * filtered["education_match"] +
        0.1 * filtered["tfidf_score"]
    )

    # Top-N results
    top_n_df = filtered.sort_values(by="final_score", ascending=False).head(top_n)

    output_cols = [c for c in [
        "job_title", "company_name", "skills", "category", 
        "job_loc", "education", "compensation", "href", "final_score"
    ] if c in top_n_df.columns]

    return top_n_df[output_cols].to_dict(orient="records")

# ---------- Health / Info Endpoint ----------
@app.get("/")
def root():
    return {
        "engine": "AI-Based-Internship-Recommendation-Engine",
        "status": "online",
        "version": "1.0.0",
        "total_internships": len(df),
        "endpoint": "/recommend"
    }

# ---------- API Endpoint ----------
@app.post("/recommend")
def recommend_api(
    fullname: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    sector_interest: str = Form(...),
    location_preference: str = Form(...)
):
    # Convert skills string into list
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]

    candidate_dict = {
        "fullname": fullname,
        "education": education,
        "skills": skills_list,
        "sector_interest": sector_interest,
        "location_preference": location_preference
    }

    recommendations = recommend_internships(candidate_dict, top_n=5)
    return JSONResponse(content={
        "candidate": fullname,
        "recommendations": recommendations
    })
