# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and Streamlit, deployed on AWS EC2 using a fully automated CI/CD pipeline with GitHub Actions and Docker.

🔗 **Live Demo:** [http://52.64.156.158:8501/](http://52.64.156.158:8501/)

---

## 📌 Overview

This system recommends movies based on content similarity — analyzing genres, cast, crew, keywords, and plot overview. Enter any movie from the TMDB 5000 dataset and get 5 personalized recommendations with posters fetched live from the TMDB API.

---

## ⚙️ How It Works

```
TMDB 5000 Dataset (movies + credits)
        ↓
Feature Engineering (genres, cast, crew, keywords, overview)
        ↓
Bag of Words + Porter Stemming (NLP)
        ↓
CountVectorizer → 5000-feature vectors
        ↓
Cosine Similarity Matrix (5000 × 5000)
        ↓
Top 5 similar movies → posters via TMDB API
```

---

## 🧠 ML Techniques Used

| Technique | Purpose |
|---|---|
| Bag of Words | Convert movie tags into numerical vectors |
| Porter Stemming | Normalize words (e.g. "dancing" → "danc") |
| CountVectorizer | Build feature matrix from tags |
| Cosine Similarity | Measure similarity between movie vectors |
| Content-Based Filtering | Recommend based on movie attributes |

---

## 🗂️ Project Structure

```
movie-recommendation-system-streamlit/
├── app.py                  # Streamlit UI + recommendation logic
├── movies.pkl              # Preprocessed movie data (Git LFS)
├── similarity.pkl          # Cosine similarity matrix (Git LFS)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container config
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions CI/CD pipeline
```

---

## 🚀 CI/CD Pipeline

Every `git push` to `main` automatically triggers the full deployment pipeline:

```
git push origin main
        ↓
GitHub Actions triggered
        ↓
SSH into AWS EC2
        ↓
git pull latest code + Git LFS files
        ↓
docker build → docker run
        ↓
App live at http://52.64.156.158:8501/
```

### GitHub Secrets Used

| Secret | Purpose |
|---|---|
| `EC2_HOST` | Public IP of EC2 instance |
| `EC2_USER` | SSH username (ubuntu) |
| `EC2_KEY` | Private key (.pem file contents) |
| `TMDB_API_KEY` | TMDB API key for fetching posters |

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core language |
| Streamlit | Web UI framework |
| Scikit-learn | CountVectorizer + Cosine Similarity |
| NLTK | Porter Stemmer for NLP |
| Pandas & NumPy | Data processing |
| TMDB API | Live movie poster fetching |
| Docker | Containerization |
| AWS EC2 | Cloud hosting (t3.micro, Ubuntu 24.04) |
| GitHub Actions | CI/CD automation |
| Git LFS | Large file storage for pkl files |

---

## 🏃 Run Locally

### Prerequisites
- Python 3.11+
- TMDB API Key ([get one free here](https://www.themoviedb.org/settings/api))

### Steps

```bash
# Clone the repository
git clone https://github.com/Prince087/movie-recommendation-system-streamlit.git
cd movie-recommendation-system-streamlit

# Pull large files
git lfs install
git lfs pull

# Install dependencies
pip install -r requirements.txt

# Set your TMDB API key
export TMDB_API_KEY="your_api_key_here"   # Linux/Mac
set TMDB_API_KEY=your_api_key_here        # Windows

# Run the app
streamlit run app.py
```

### Run with Docker

```bash
docker build -t movie-recommender .
docker run -p 8501:8501 -e TMDB_API_KEY="your_key" movie-recommender
```

---

## 📊 Dataset

- **Source:** [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle)
- **Size:** 4,806 movies after preprocessing
- **Features used:** title, overview, genres, keywords, cast (top 3), crew (director)

---

## 🔒 Security

- API keys stored as encrypted GitHub Secrets — never hardcoded in source
- Docker `-e` flag injects secrets at runtime as environment variables
- Keys are masked as `***` in all GitHub Actions logs

---

## 👨💻 Author

**Prince** — [GitHub](https://github.com/Prince087)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
