from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load Internship Dataset ----------
df = pd.read_csv("internships.csv")

# ---------- Utility: Jaccard Similarity ----------
def jaccard_similarity(set1, set2):
    set1, set2 = set(set1), set(set2)
    inter = len(set1 & set2)
    union = len(set1 | set2)
    return inter / union if union > 0 else 0

# ---------- Core Recommendation ----------
def recommend_internships(candidate: dict, top_n: int = 5):
    filtered = df.copy()

    # Rule-based soft matches
    filtered["sector_match"] = filtered["category"].str.contains(
        candidate.get("sector_interest", ""), case=False, na=False
    ).astype(int)

    filtered["location_match"] = filtered["job_loc"].str.contains(
        candidate.get("location_preference", ""), case=False, na=False
    ).astype(int)

    filtered["education_match"] = filtered["education"].str.contains(
        candidate.get("education", ""), case=False, na=False
    ).astype(int)

    # Jaccard skill similarity
    scores = []
    for _, row in filtered.iterrows():
        internship_skills = [s.strip() for s in str(row["skills"]).split(",")]
        score = jaccard_similarity(candidate.get("skills", []), internship_skills)
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
        " ".join(candidate.get("skills", [])) + " " +
        candidate.get("sector_interest", "") + " " +
        candidate.get("location_preference", "") + " " +
        candidate.get("education", "")
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

    return top_n_df[[
        "job_title", "skills", "category", "job_loc", "education", "final_score"
    ]].to_dict(orient="records")

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
    return JSONResponse(content={"recommendations": recommendations})
