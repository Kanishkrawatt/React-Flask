# Customized Learning Resources Dashboard

Build a dashboard that aggregates learning resources from different platforms and presents them to the user based on their preferences, learning style, and areas of interest.

## Getting Started

For this project , I used the following technologies:

- Frontend: React JS
- Backend: Flask (Python)
- Dataset: Kaggle
- ML monel: Cosine Similarity (NLP)

### Why Cosine Similarity?

Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. In this case, the two vectors I am referring to are arrays containing the word counts of two documents.

### Installation

- Clone the repo

```sh
git clone
```

- Install NPM packages

```sh
npm install
```

- Install Python packages

```sh
pip install -r requirements.txt
```

- Run the app

```sh
npm start
```

- Run the backend server

```sh
cd server
# create a virtual environment
python3 -m venv .venv # Linux
py -3 -m venv .venv # Windows

# first activate the virtual environment
. .venv/bin/active # Linux
.venv\Scripts\activate  # Windows

# run the server
flask --app server.py run
or 
python -m flask --app server.py run
```
