from flask import Flask
from flask_cors import CORS
from markupsafe import escape
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Welcome to the server!"


@app.route("/coursera/<subject>/<difficulty>/")
def recommend_coursera(subject, difficulty):
    subject = escape(subject.replace("-", " "))
    difficulty = escape(difficulty.capitalize())
    data = get_recommendations_coursera(subject=subject, course_difficulty=difficulty)
    return {"data": data}


@app.route("/udemy/<subject>/<difficulty>/")
def recommend_udemy(subject, difficulty):
    subject = escape(subject.replace("-", " "))
    difficulty = escape(difficulty.replace("-", " "))
    data = get_recommendations_udemy(subject=subject, course_difficulty=difficulty)
    return {"data": data}


def get_recommendations_coursera(subject="AI", course_difficulty="Intermediate"):
    df_coursera = pd.read_csv("../data/data.csv")
    df_coursera["features"] = (
        df_coursera["course_difficulty"]
        + " "
        + df_coursera["course_title"]
        + " "
        + df_coursera["course_organization"]
    )

    tfidf_vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix_coursera = tfidf_vectorizer.fit_transform(df_coursera["features"])
    cosine_sim_coursera = linear_kernel(tfidf_matrix_coursera, tfidf_matrix_coursera)

    user_course_index = df_coursera.index[
        (df_coursera["course_difficulty"] == course_difficulty)
        & (df_coursera["features"].str.contains(subject))
    ].tolist()
    similarity_scores = []
    for i in user_course_index:
        similarity_scores.append(list(enumerate(cosine_sim_coursera[i])))
    sums = {}
    counts = {}
    for inner_list in similarity_scores:
        for tup in inner_list:
            index, score = tup
            sums[index] = sums.get(index, 0) + score
            counts[index] = counts.get(index, 0) + 1

    avg_similarity_scores = [(index, sums[index] / counts[index]) for index in sums]

    weighted_scores = [
        (i, score * df_coursera["course_rating"][i])
        for i, score in avg_similarity_scores
    ]
    weighted_scores = sorted(weighted_scores, key=lambda x: x[1], reverse=True)

    arr = []
    for i in weighted_scores[0:11]:
        arr.append(
            {
                "course_title": df_coursera["course_title"][i[0]],
                "course_organization": df_coursera["course_organization"][i[0]],
                "course_rating": df_coursera["course_rating"][i[0]],
                "course_difficulty": df_coursera["course_difficulty"][i[0]],
                "course_students_enrolled": df_coursera["course_students_enrolled"][
                    i[0]
                ],
            }
        )
    return arr


def get_recommendations_udemy(subject="AI", course_difficulty="Intermediate"):
    df_udemy = pd.read_csv("../data/udemy_courses.csv")
    df_udemy["features"] = df_udemy["level"] + " " + df_udemy["course_title"]

    tfidf_vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix_udemy = tfidf_vectorizer.fit_transform(df_udemy["features"])
    cosine_sim_udemy = linear_kernel(tfidf_matrix_udemy)

    user_course_index = df_udemy.index[
        (df_udemy["level"] == course_difficulty)
        & (df_udemy["features"].str.contains(subject))
    ].tolist()
    similarity_scores = []
    for i in user_course_index:
        similarity_scores.append(list(enumerate(cosine_sim_udemy[i])))

    sums = {}
    counts = {}
    for inner_list in similarity_scores:
        for tup in inner_list:
            index, score = tup
            sums[index] = sums.get(index, 0) + score
            counts[index] = counts.get(index, 0) + 1

    avg_similarity_scores = [(index, sums[index] / counts[index]) for index in sums]

    weighted_scores = sorted(avg_similarity_scores, key=lambda x: x[1], reverse=True)

    arr = []
    for i in weighted_scores[0:11]:  # Exclude the input course itself
        arr.append(
            {
                "course_title": df_udemy["course_title"][i[0]],
                "url": df_udemy["url"][i[0]],
                "level": df_udemy["level"][i[0]],
                "is_paid": str(df_udemy["is_paid"][i[0]]),
                "price": str(df_udemy["price"][i[0]]),
            }
        )
    return arr


if __name__ == "__main__":
    app.run(debug=True, port=8001)
