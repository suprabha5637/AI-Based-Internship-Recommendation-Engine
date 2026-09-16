# 🎓 AI-Based Internship Recommendation Engine

An **AI-powered Internship Recommendation Engine** developed for the **Smart India Hackathon (SIH)** to help students discover internship opportunities that best match their **skills, education, preferred sector, and location**.

The system combines **Rule-Based Matching, Jaccard Similarity, and TF-IDF/Cosine Similarity** to generate personalized internship recommendations and return the **top 5 matching opportunities**.

---

## 🚀 Project Overview

Finding the right internship can be difficult for students because thousands of opportunities may be available across different domains, locations, and qualification requirements.

This project solves that problem by analyzing a student's profile and comparing it with available internship opportunities.

### 👨‍🎓 Student provides:

* Full Name
* Educational Qualification
* Skills
* Sector of Interest
* Preferred Location

### 🤖 Recommendation Engine analyzes:

* Skill similarity
* Sector/category match
* Location preference
* Educational qualification
* Textual similarity between the candidate profile and internship information

### 🎯 Output:

The system returns the **Top 5 recommended internships**, along with a calculated **match score**.

---

## ✨ Key Features

* 🎯 Personalized internship recommendations
* 🤖 Hybrid AI recommendation algorithm
* 🧠 Jaccard Similarity for skill matching
* 📊 TF-IDF + Cosine Similarity for textual matching
* 📋 Rule-based filtering and matching
* 📍 Location-based matching
* 🎓 Education-based matching
* 💼 Sector/category matching
* ⭐ Match percentage for every recommendation
* 🌐 Interactive web interface
* 🗺️ Interactive India map using Leaflet
* 🔎 Internship search and filtering
* 📱 Responsive frontend interface
* ⚡ FastAPI REST API
* 📁 CSV-based internship dataset

---

# 🧠 Recommendation System

The core of the project is a **Hybrid Recommendation Engine**.

Instead of relying on a single algorithm, the system combines multiple matching techniques to produce a more meaningful recommendation score.

## 1. Jaccard Similarity

Jaccard Similarity is used to compare the student's skills with the skills required by an internship.

### Formula

```text
Jaccard Similarity =
|Intersection of Skills|
------------------------
|Union of Skills|
```

For example:

```text
Student Skills:
Python, SQL, Machine Learning

Internship Skills:
Python, SQL, MongoDB
```

Common skills:

```text
Python, SQL
```

The algorithm calculates the similarity between both skill sets.

---

## 2. Rule-Based Matching

The system checks whether the student's preferences match the internship.

### Sector Match

Checks whether the selected sector appears in the internship category.

```text
Sector Match = 1 → Match
Sector Match = 0 → No Match
```

### Location Match

Checks whether the preferred location appears in the internship location.

```text
Location Match = 1 → Match
Location Match = 0 → No Match
```

### Education Match

Checks whether the student's educational qualification matches the internship requirement.

```text
Education Match = 1 → Match
Education Match = 0 → No Match
```

---

## 3. TF-IDF Similarity

The system also uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to understand textual similarity between the candidate profile and internship information.

The internship text is constructed from:

```text
Skills
+
Category
+
Education
+
Location
```

The candidate profile is constructed from:

```text
Skills
+
Sector Interest
+
Preferred Location
+
Education
```

The system then calculates **Cosine Similarity** between the candidate profile and internship records.

---

# 📐 Hybrid Scoring Formula

The final recommendation score is calculated using the following weighted formula:

```text
Final Score =
    0.5 × Jaccard Skill Score
  + 0.2 × Sector Match
  + 0.1 × Location Match
  + 0.1 × Education Match
  + 0.1 × TF-IDF Similarity
```

### Weight Distribution

| Component                   |   Weight |
| --------------------------- | -------: |
| 🧠 Jaccard Skill Similarity |      50% |
| 💼 Sector Match             |      20% |
| 📍 Location Match           |      10% |
| 🎓 Education Match          |      10% |
| 📊 TF-IDF Similarity        |      10% |
| **Total**                   | **100%** |

The internships are then sorted by their final score and the **top 5 results** are returned.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Student         │
                    │  Profile Information │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Web Frontend      │
                    │ HTML / CSS / JS      │
                    └──────────┬───────────┘
                               │
                         HTTP POST
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │      /recommend      │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌──────────────────────────┐
                  │ Recommendation Engine    │
                  │                          │
                  │ • Rule-Based Matching    │
                  │ • Jaccard Similarity     │
                  │ • TF-IDF                │
                  │ • Cosine Similarity     │
                  └────────────┬─────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Internship Dataset   │
                    │     internships.csv  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Top 5 Internships  │
                    │   + Match Percentage │
                    └──────────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

* **Python**
* **FastAPI**
* **Uvicorn**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **TF-IDF Vectorizer**
* **Cosine Similarity**

## Frontend

* **HTML5**
* **CSS3**
* **JavaScript**
* **Leaflet.js**
* **OpenStreetMap**

## Data

* **CSV Dataset**
* `internships.csv`

## Machine Learning / NLP

* Jaccard Similarity
* TF-IDF
* Cosine Similarity
* Hybrid Recommendation Algorithm
* Rule-Based Matching

---

# 📂 Project Structure

```text
AI-Based-Internship-Recommendation-Engine-SIH/
│
├── app/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── cards.html
│   └── recommend.html
│
├── internships.csv
│
├── requirements.txt
│
├── sih_with_Rule_based_+_Jaccard_+_TF_IDF_hybrid_recommender.ipynb
│
├── .gitattributes
│
└── README.md
```

---

# 📄 File Description

### `app/main.py`

Main FastAPI backend.

Responsibilities:

* Loads internship dataset
* Processes candidate information
* Calculates Jaccard similarity
* Performs rule-based matching
* Calculates TF-IDF similarity
* Calculates final hybrid score
* Returns top 5 internships through the API

---

### `internships.csv`

Contains internship information such as:

```text
ID
Job Title
Company Name
Location
Details
Category
Compensation
Start Date
End Date
Skills
Application Link
Education
```

---

### `frontend/index.html`

Main frontend interface for collecting student information and displaying recommendations.

---

### `frontend/cards.html`

Internship dashboard containing:

* Internship categories
* Search
* Location filtering
* Internship cards
* India map
* Apply buttons

---

### `frontend/recommend.html`

Frontend page for displaying personalized internship recommendations.

---

### `sih_with_Rule_based_+_Jaccard_+_TF_IDF_hybrid_recommender.ipynb`

Jupyter Notebook containing experimentation and development of the hybrid recommendation approach.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Based-Internship-Recommendation-Engine-SIH.git
```

Move into the project directory:

```bash
cd AI-Based-Internship-Recommendation-Engine-SIH
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

# 📦 Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The project uses:

```text
fastapi
uvicorn
python-multipart
pandas
scikit-learn
numpy
```

---

# ▶️ Run the Backend

From the project root directory:

```bash
uvicorn app.main:app --reload
```

The backend will start at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 🔌 API

## POST `/recommend`

Generates personalized internship recommendations.

### Request Parameters

| Parameter             | Description                 |
| --------------------- | --------------------------- |
| `fullname`            | Student's full name         |
| `education`           | Educational qualification   |
| `skills`              | Comma-separated skills      |
| `sector_interest`     | Preferred internship sector |
| `location_preference` | Preferred location          |

### Example

```text
fullname = Suprabha Kundu
education = B.Tech Computer Science
skills = Python, SQL, Machine Learning
sector_interest = Software Developer
location_preference = Bangalore
```

---

# 📤 Example API Response

```json
{
  "recommendations": [
    {
      "job_title": "Software Developer",
      "skills": "Go, Java, MongoDB, Nginx, Python",
      "category": "Software Developer : Python",
      "job_loc": "Bangalore",
      "education": "B.Tech Computer Science",
      "final_score": 0.78
    }
  ]
}
```

The frontend converts the final score into a percentage.

For example:

```text
0.78 → 78%
```

---

# 🎨 User Workflow

```text
1. Open the internship recommendation page
              ↓
2. Enter personal information
              ↓
3. Enter education qualification
              ↓
4. Enter skills
              ↓
5. Select/enter sector of interest
              ↓
6. Enter preferred location
              ↓
7. Click "Get Recommendations"
              ↓
8. Frontend sends data to FastAPI
              ↓
9. Recommendation engine processes profile
              ↓
10. Hybrid score is calculated
              ↓
11. Internships are ranked
              ↓
12. Top 5 recommendations are displayed
```

---

# 🌐 Frontend Features

## 🔍 Internship Search

Users can search internships based on keywords.

Example:

```text
Python
Web Development
Marketing
Finance
AI
```

---

## 📍 Location Filtering

The dashboard provides location-based filtering for cities such as:

* Delhi
* Mumbai
* Bangalore
* Chennai
* Hyderabad
* Pune
* Kolkata
* Ahmedabad
* Jaipur
* Lucknow
* Chandigarh
* Bhopal
* Indore
* Guwahati
* Patna
* Gurgaon
* Noida

---

## 🗺️ Interactive India Map

The project uses **Leaflet.js** and **OpenStreetMap** to display internship-related locations on an interactive India map.

Users can interact with city markers and use them to filter internship opportunities.

---

# 💡 Why a Hybrid Recommendation System?

A single recommendation technique may not be sufficient for internship matching.

For example:

### Skill similarity alone

A student may have the required technical skills but may not prefer the internship location.

### Location matching alone

An internship may be in the student's preferred city but may require completely different skills.

### Keyword matching alone

Simple keyword matching may miss semantic relationships between different pieces of information.

Therefore, this project combines:

```text
Skill Matching
       +
Sector Matching
       +
Location Matching
       +
Education Matching
       +
Text Similarity
       ↓
Hybrid Recommendation Score
```

This provides a multi-factor approach to internship recommendation.

---

# 📊 Example

Suppose a student enters:

```text
Education:
B.Tech Computer Science

Skills:
Python, SQL, Machine Learning

Sector:
Software Developer

Location:
Bangalore
```

The system evaluates every internship using:

```text
Skill Similarity
        +
Sector Match
        +
Location Match
        +
Education Match
        +
TF-IDF Similarity
```

The internships are ranked according to the final score.

The system then returns:

```text
🥇 Recommendation 1
🥈 Recommendation 2
🥉 Recommendation 3
4️⃣ Recommendation 4
5️⃣ Recommendation 5
```

Each recommendation includes a match percentage.

---

# 🔐 CORS Configuration

The FastAPI backend includes CORS middleware to allow communication between the frontend and backend during development.

The current implementation allows:

```text
All origins
All methods
All headers
```

For production deployment, CORS should be restricted to trusted frontend domains.

---

# 🚀 Future Improvements

The current prototype can be extended into a production-ready recommendation platform.

### 🤖 Advanced AI

* Transformer-based embeddings
* Sentence Transformers
* Semantic Search
* Large Language Models
* Personalized recommendation models
* Learning-to-Rank algorithms

### 👤 User Profiles

* Student registration/login
* Persistent user profiles
* Resume upload
* Automatic skill extraction
* Education extraction
* Experience tracking

### 📄 Resume-Based Recommendation

Users could upload a resume:

```text
Resume
  ↓
Resume Parser
  ↓
Skill Extraction
  ↓
Education Extraction
  ↓
Experience Extraction
  ↓
AI Recommendation Engine
  ↓
Personalized Internships
```

### 📈 Recommendation Analytics

Future versions could track:

* Click-through rate
* Applications
* Saved internships
* User preferences
* Recommendation accuracy
* Internship conversion rate

### ☁️ Cloud Deployment

Possible production deployment:

```text
Frontend
   ↓
Cloud Hosting
   ↓
FastAPI Backend
   ↓
Recommendation Service
   ↓
Database
```

Potential platforms include:

* AWS
* Google Cloud
* Microsoft Azure
* Vercel
* Render

---

# 🧪 Testing

The recommendation algorithm can be tested using different candidate profiles.

### Example Test Cases

#### Test Case 1 — Software Development

```text
Education: B.Tech Computer Science
Skills: Python, Java, SQL
Sector: Software Developer
Location: Bangalore
```

#### Test Case 2 — Marketing

```text
Education: MBA
Skills: Marketing, Communication, SEO
Sector: Marketing
Location: Mumbai
```

#### Test Case 3 — Finance

```text
Education: B.Com
Skills: Finance, Accounting, Excel
Sector: Finance
Location: Kolkata
```

These profiles should produce different recommendation rankings.

---

# 📌 Current Project Status

```text
✅ Frontend implemented
✅ FastAPI backend implemented
✅ Internship dataset integrated
✅ Jaccard similarity implemented
✅ Rule-based matching implemented
✅ TF-IDF implemented
✅ Cosine similarity implemented
✅ Hybrid scoring implemented
✅ Top-5 recommendations implemented
✅ Location filtering implemented
✅ Interactive map implemented
```

---

# 🎯 Project Objective

The primary objective of this project is to create an intelligent internship discovery system that reduces the difficulty students face when searching through large numbers of internship opportunities.

By combining multiple recommendation techniques, the system attempts to connect students with internship opportunities that better align with their:

```text
Skills
Education
Career Interests
Location Preferences
```

---

# 🏆 Smart India Hackathon

This project was developed as a solution concept for the **Smart India Hackathon (SIH)** with the goal of applying artificial intelligence and recommendation technologies to improve internship discovery and career opportunities for students.

---

# 👨‍💻 Technologies Used

```text
Python
FastAPI
Uvicorn
Pandas
NumPy
Scikit-learn
TF-IDF
Cosine Similarity
Jaccard Similarity
HTML5
CSS3
JavaScript
Leaflet.js
OpenStreetMap
Jupyter Notebook
Git
GitHub
```

---

# 📜 License

This project is intended for educational, research, and hackathon purposes.

If you reuse or extend this project, please provide appropriate attribution to the original project and contributors.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 🚀 Built with Python, Machine Learning & ❤️

**AI-Based Internship Recommendation Engine — Smart Internship Discovery for Students**
