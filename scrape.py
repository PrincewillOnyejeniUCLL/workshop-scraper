import requests
import pandas as pd
from supabase import create_client
from datetime import datetime

# ------------------------
# 1. SCRAPE DATA
# ------------------------
url = "https://www.arbeitnow.com/api/job-board-api"

response = requests.get(url)
data = response.json()
jobs = data["data"]

job_list = []

for job in jobs:
    job_list.append({
        "title": job["title"],
        "company": job["company_name"],
        "location": job["location"],
        "tags": ", ".join(job["tags"]),
        "description": job["description"]
    })

df = pd.DataFrame(job_list)

print(f"✅ Scraped {len(df)} jobs")

# ------------------------
# 2. CLEAN DATA (ADD SKILLS)
# ------------------------
skills = ["Python", "JavaScript", "SQL", "AWS", "Docker", "React"]

for skill in skills:
    df[skill] = df["tags"].str.contains(skill, case=False, na=False)

# ------------------------
# 3. ADD TIMESTAMP
# ------------------------
scraped_at = datetime.now().isoformat()

# ------------------------
# 4. SUPABASE CONNECTION
# ------------------------
SUPABASE_URL = "https://voqikgvnbuovdnnzbypc.supabase.co"
SUPABASE_KEY = "sb_publishable_xLeHKq49TXtk_Si7GB3Acw_6BvUxdjl"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------
# 5. PREPARE DATA FOR INSERT
# ------------------------
rows = []

for _, row in df.iterrows():
    rows.append({
        "title": row["title"],
        "company": row["company"],
        "location": row["location"],
        "tags": row["tags"],
        "description": row["description"],
        "python": bool(row["Python"]),
        "javascript": bool(row["JavaScript"]),
        "sql": bool(row["SQL"]),
        "aws": bool(row["AWS"]),
        "docker": bool(row["Docker"]),
        "react": bool(row["React"]),
        "scraped_at": scraped_at
    })

# ------------------------
# 6. INSERT INTO DATABASE
# ------------------------
result = supabase.table("jobs").insert(rows).execute()

print(f"✅ Inserted {len(rows)} rows into Supabase")
