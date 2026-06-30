import zipfile

zip_path = "/content/[PUB] India_runs_data_and_ai_challenge.zip"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("/content/challenge")

print("Files extracted successfully!")
import os

for root, dirs, files in os.walk("/content/challenge"):
    for file in files:
        print(os.path.join(root, file))
import json

path = "/content/challenge/[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/candidates.jsonl"

with open(path, "r", encoding="utf-8") as f:
    for i in range(3):
        candidate = json.loads(f.readline())
        print(candidate)
        print("=" * 80)
!pip install pandas tqdm
import json
import pandas as pd
from tqdm import tqdm

FILE = "/content/challenge/[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/candidates.jsonl"

TARGET_SKILLS = [
    "Python","LLM","Fine-tuning LLMs","RAG","NLP",
    "Milvus","Vector Database","Embeddings",
    "BentoML","Kafka","Spark","AWS","GCP"
]

results = []

with open(FILE, "r", encoding="utf-8") as f:
    for line in tqdm(f):
        c = json.loads(line)

        score = 0

        # Experience
        exp = c["profile"]["years_of_experience"]
        if 5 <= exp <= 9:
            score += 30

        # Skills
        skills = [s["name"] for s in c["skills"]]
        for t in TARGET_SKILLS:
            if t in skills:
                score += 5

        # Open to work
        if c["redrob_signals"]["open_to_work_flag"]:
            score += 10

        # GitHub activity
        gh = c["redrob_signals"]["github_activity_score"]
        if gh > 0:
            score += gh

        results.append({
            "candidate_id": c["candidate_id"],
            "score": score
        })

df = pd.DataFrame(results)

df = df.sort_values("score", ascending=False)

df = df.head(100)

df["rank"] = range(1,101)

df["reasoning"] = "Strong AI Engineer profile"

submission = df[["candidate_id","rank","score","reasoning"]]

submission.to_csv("submission.csv", index=False)

print(submission.head())
!python "/content/challenge/[PUB] India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/validate_submission.py" \
--submission submission.csv