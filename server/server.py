from flask import Flask
from markupsafe import escape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to the server!"


@app.route("/recommend/<subject>/<difficulty>")
def recommend(subject, difficulty):
    subject = escape(subject.replace("-", " "))
    difficulty = escape(difficulty.capitalize())
    data = get_recommendations(
        subject=subject, course_difficulty=difficulty
    )
    if len(data) == 0:
        return {"data": "No courses found!"}
    return {"data": data}


df = pd.read_csv("../data/data.csv")

df["features"] = (
    df["course_difficulty"] + " " + df["course_title"] + " " + df["course_organization"]
)

tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(df["features"])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(
    subject="AI", course_difficulty="Intermediate", cosine_sim=cosine_sim
):
    user_course_index = df.index[
        (df["course_difficulty"] == course_difficulty)
        & (df["features"].str.contains(subject))
    ].tolist()[0]

    similarity_scores = list(enumerate(cosine_sim[user_course_index]))

    weighted_scores = [
        (i, score * df["course_rating"][i]) for i, score in similarity_scores
    ]
    weighted_scores = sorted(weighted_scores, key=lambda x: x[1], reverse=True)

    arr = []
    for i in weighted_scores[1:6]:  # Exclude the input course itself
        arr.append(
            {
                "course_title": df["course_title"][i[0]],
                "course_organization": df["course_organization"][i[0]],
                "course_rating": df["course_rating"][i[0]],
                "course_difficulty": df["course_difficulty"][i[0]],
                "course_students_enrolled": df["course_students_enrolled"][i[0]],
            }
        )
    return arr


if __name__ == "__main__":
    app.run(debug=True, port=8001)
