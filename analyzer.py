import pandas as pd
import matplotlib.pyplot as plt
import os

# Create outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Load dataset
df = pd.read_csv("data/jobs.csv")

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

# =====================================================
# Insight 1: Top 10 Cities with Most Job Postings
# =====================================================

top_cities = df["location"].value_counts().head(10)

print("\nTop 10 Cities with Most Job Postings:")
print(top_cities)

plt.figure(figsize=(10, 5))
top_cities.plot(kind="bar")
plt.title("Top 10 Hiring Cities")
plt.xlabel("City")
plt.ylabel("Number of Job Postings")
plt.tight_layout()
plt.savefig("outputs/top_hiring_cities.png")
plt.show()

# =====================================================
# Insight 2: Top 10 Hiring Companies
# =====================================================

top_companies = df["companyName"].value_counts().head(10)

print("\nTop 10 Hiring Companies:")
print(top_companies)

plt.figure(figsize=(12, 5))
top_companies.plot(kind="bar")
plt.title("Top 10 Hiring Companies")
plt.xlabel("Company")
plt.ylabel("Number of Job Postings")
plt.tight_layout()
plt.savefig("outputs/top_hiring_companies.png")
plt.show()

# =====================================================
# Insight 3: Top 20 Demanded Skills
# =====================================================

skills = []

for row in df["tagsAndSkills"].dropna():
    skills.extend(str(row).split(","))

# Remove extra spaces
skills = [skill.strip() for skill in skills]

skill_counts = pd.Series(skills).value_counts().head(20)

print("\nTop 20 Demanded Skills:")
print(skill_counts)

plt.figure(figsize=(12, 5))
skill_counts.plot(kind="bar")
plt.title("Top 20 Demanded Skills")
plt.xlabel("Skills")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/top_demanded_skills.png")
plt.show()

# =====================================================
# Insight 4: Salary Distribution
# =====================================================

df["averageSalary"] = (
    pd.to_numeric(df["minimumSalary"], errors="coerce")
    + pd.to_numeric(df["maximumSalary"], errors="coerce")
) / 2

print("\nSalary Statistics:")
print(df["averageSalary"].describe())

plt.figure(figsize=(10, 5))
plt.hist(df["averageSalary"].dropna(), bins=20)
plt.title("Salary Distribution")
plt.xlabel("Average Salary")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.savefig("outputs/salary_distribution.png")
plt.show()

# =====================================================
# Insight 5: Experience vs Salary
# =====================================================

df["averageExperience"] = (
    pd.to_numeric(df["minimumExperience"], errors="coerce")
    + pd.to_numeric(df["maximumExperience"], errors="coerce")
) / 2

plt.figure(figsize=(10, 5))
plt.scatter(
    df["averageExperience"],
    df["averageSalary"]
)
plt.title("Experience vs Salary")
plt.xlabel("Average Experience (Years)")
plt.ylabel("Average Salary")
plt.tight_layout()
plt.savefig("outputs/experience_vs_salary.png")
plt.show()

# =====================================================
# Career Recommendation Tool
# =====================================================

career = input("\nEnter a role (Example: Data Analyst): ")

filtered = df[
    df["title"]
    .str.contains(career, case=False, na=False)
]

if filtered.empty:
    print("\nNo matching roles found.")
else:
    role_skills = []

    for row in filtered["tagsAndSkills"].dropna():
        role_skills.extend(str(row).split(","))

    role_skills = [skill.strip() for skill in role_skills]

    recommendations = (
        pd.Series(role_skills)
        .value_counts()
        .head(10)
    )

    print(f"\nTop Skills Required for '{career}':")
    print(recommendations)

    plt.figure(figsize=(10, 5))
    recommendations.plot(kind="bar")
    plt.title(f"Top Skills for {career}")
    plt.xlabel("Skills")
    plt.ylabel("Frequency")
    plt.tight_layout()

    filename = career.lower().replace(" ", "_")
    plt.savefig(f"outputs/{filename}_skills.png")

    plt.show()

# =====================================================
# Project Complete
# =====================================================

print("\nAnalysis Complete!")
print("All visualizations have been saved in the 'outputs' folder.")
