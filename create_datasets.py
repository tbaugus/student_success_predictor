import pandas as pd
import numpy as np
from pathlib import Path

# Set seed for reproducibility
np.random.seed(42)
n_students = 7500

# 1. Create Student Registry
student_ids = np.random.choice(range(10000, 99999), n_students, replace=False)

students = pd.DataFrame({
    'student_id': student_ids,
    'major': np.random.choice(['Computer Science', 'CS', 'CompSci', 'Mathematics', 'Business', 'Arts'], n_students),
    # More realistic: mostly 18-25 with a smaller adult-learner segment.
    'age': np.clip(
        np.round(
            np.where(
                np.random.rand(n_students) < 0.82,
                np.random.normal(loc=21.5, scale=2.3, size=n_students),  # traditional students
                np.random.normal(loc=31.0, scale=5.5, size=n_students),  # adult learners
            )
        ),
        17,
        50,
    ).astype(int),
    'gender': np.random.choice(['Male', 'Female', 'Non-binary', 'Prefer not to say'], n_students, p=[0.48, 0.48, 0.02, 0.02]),
    'prior_gpa': np.round(np.random.uniform(2.0, 4.0, n_students), 2),
    'credits_failed_pct': np.random.beta(1, 5, n_students),
    'financial_aid': np.random.choice(['Federal Grant', 'Private Scholarship', 'Student Loan', 'No Aid'], n_students),
    'tuition_status': np.random.choice(['Paid', 'Deferred', 'Delinquent'], n_students, p=[0.7, 0.2, 0.1])
})

# --- SCATTERED ERRORS CHUNK ---
error_indices_age = np.random.choice(students.index, size=50, replace=False)
error_indices_gpa = np.random.choice(students.index, size=50, replace=False)
error_indices_nan = np.random.choice(students.index, size=100, replace=False)

students.loc[error_indices_age, 'age'] = -1
students.loc[error_indices_gpa, 'prior_gpa'] = 5.5
students.loc[error_indices_nan, 'financial_aid'] = np.nan

# 2. Create Engagement Logs (Q1-Q3)
# Using index to exclude 300 "Ghost" students
active_indices = students.index[:-300]
rows = []

for idx in active_indices:
    s_info = students.loc[idx]
    sid = s_info['student_id']

    # Logic for socio-economic slump
    is_at_risk = (s_info['financial_aid'] == 'No Aid') and (s_info['tuition_status'] == 'Delinquent')

    for q in ['Q1', 'Q2', 'Q3']:
        base_time = np.random.randint(50, 250)

        if q == 'Q3' and is_at_risk:
            base_time = int(base_time * 0.6)

        # Logins: 1 per ~20 mins of study
        logins = max(1, int(base_time / np.random.randint(15, 30)))

        # Forum Posts: Poisson distribution weighted by engagement
        forum_posts = np.random.poisson(lam=(base_time / 100))

        rows.append({
            'student_id': sid,
            'quarter': q,
            'time_on_materials_min': base_time,
            'logins': logins,
            'forum_posts': forum_posts
        })

engagement = pd.DataFrame(rows)

# 3. Create Target Labels
students['graduated'] = 1
dropout_probs = (students['credits_failed_pct'] * 0.8) + (np.random.rand(n_students) * 0.2)
students.loc[dropout_probs > 0.4, 'graduated'] = 0
# Explicitly setting ghost student outcomes
students.loc[students.index[-300:], 'graduated'] = np.random.choice([0, 1], 300, p=[0.93, 0.07])

# Save files
BASE_DIR = Path(__file__).resolve().parent
registry_out = BASE_DIR / "student_registry.csv"
engagement_out = BASE_DIR / "engagement_data.csv"

students.to_csv(registry_out, index=False)
engagement.to_csv(engagement_out, index=False)
print(f"Files generated: {registry_out.name}, {engagement_out.name}")
