# Data dictionary: `student_registry_cleaned_features.csv`

| Field | Value |
|-------|--------|
| **Dataset file** | `data/student_registry_cleaned_features.csv` |
| **Grain** | One row per student |
| **Row count** | 7,400 (as of last export; 7,500 registry rows minus 100 with missing `financial_aid`) |
| **Column count** | 27 |
| **Primary key** | `student_id` |
| **Data nature** | **Synthetic** (not real students). Suitable for methods development and pipeline testing. |
| **Modeling intent** | Features reflect a **snapshot after the third quarter of the senior year** (three LMS quarters of engagement: Q1–Q3 of that academic year). The target is whether the student **graduates**. The goal is to support **late interventions in the fourth (final) quarter** to improve outcomes. |
| **Lineage** | Built in `01_Wrangling_Exploration.ipynb`: cleaned registry → left merge with wide LMS engagement → `fillna(0)` on engagement columns → derived metrics, flags, and interaction features → exported with `df_master.to_csv(data_dir / "student_registry_cleaned_features.csv")`. |

---

## Project assumptions (synthetic data; confirmed)

- **`student_id`:** Synthetic identifiers. In the notebook, IDs are cast to **string** for joins and so the key is **not treated as a numeric feature** in summaries or the predictive model (if the CSV is read back as integer, re-cast to string or drop from features).
- **`credits_failed_pct`:** Synthetic. Interpreted as **classes failed ÷ all classes taken over the college career** (proportion).
- **`graduated`:** **`1` = graduated**, **`0` = did not graduate**. Framed as **historical** rows: registry and engagement stats as of **senior year**, with outcome known after graduation.
- **`gender`, `financial_aid`, `tuition_status`:** Synthetic only; **no** institutional source or policy attached.
- **Engagement metrics:** Treated as coming from the **LMS**. The institution uses **four quarters per academic year**; this file contains **three quarters** of LMS activity (Q1–Q3) aligned to the senior-year intervention story. Missing engagement after merge is filled with **`0`**: every registry student remains in the file, including those who **never logged in**, so engagement is explicitly **zero** rather than missing—graduation/non-graduation can still be used for signal (`is_ghost` captures no-login students).

---

## Column reference

| Column | Storage type (CSV) | Description | Provenance / transformation |
|--------|-------------------|-------------|----------------------------|
| `student_id` | String or integer\* | Synthetic unique student key. | Loaded from `student_registry.csv`; cast to **string** in-notebook for merges and to keep out of numeric summaries / modeling. \*CSV readers may infer integer if values are all digits. |
| `major` | String | Academic major / program. | Registry; **standardized**: CS variants (`cs`, `compsci`, `computer science`, case- and whitespace-insensitive) → **`Computer Science`**. Levels: Arts, Business, Computer Science, Mathematics. |
| `age` | Float | Age in years. | Sentinel **`age == -1`** → missing; imputed with **median age within `major`**. |
| `gender` | String | Gender category (synthetic). | Registry; no transformation. Levels: Female, Male, Non-binary, Prefer not to say. |
| `prior_gpa` | Float | Prior cumulative GPA (0–4 scale). | Values **outside \[0.0, 4.0\]** → missing; imputed with **median `prior_gpa` within `major`**. |
| `credits_failed_pct` | Float | Proportion of **classes failed** over **all classes taken in college** (synthetic). | Registry; **unchanged** in notebook. |
| `financial_aid` | String | Aid category (synthetic). | Registry; rows with **missing `financial_aid` dropped** before merge. Levels: Federal Grant, No Aid, Private Scholarship, Student Loan. |
| `tuition_status` | String | Tuition / account standing (synthetic). | Registry; no transformation. Levels: Deferred, Delinquent, Paid. |
| `graduated` | Integer (0/1) | **1** = graduated, **0** = did not graduate (synthetic outcome). | Registry; represents historical outcome for the senior-year snapshot use case. |
| `logins_q1` | Float | LMS login count, senior-year **Q1**. | From `engagement_data.csv`, pivoted wide. Missing → **0** with other `*_q*` engagement fields. |
| `logins_q2` | Float | LMS logins, Q2. | Same as `logins_q1`. |
| `logins_q3` | Float | LMS logins, Q3. | Same as `logins_q1`. |
| `time_on_materials_min_q1` | Float | Minutes on course materials, Q1. | Same pipeline as logins. |
| `time_on_materials_min_q2` | Float | Minutes on materials, Q2. | Same pipeline as logins. |
| `time_on_materials_min_q3` | Float | Minutes on materials, Q3. | Same pipeline as logins. |
| `forum_posts_q1` | Float | Forum posts, Q1. | Same pipeline as logins. |
| `forum_posts_q2` | Float | Forum posts, Q2. | Same pipeline as logins. |
| `forum_posts_q3` | Float | Forum posts, Q3. | Same pipeline as logins. |
| `login_velocity` | Float | Change in logins Q1 → Q3. | **`logins_q3 - logins_q1`** |
| `time_velocity` | Float | Change in study minutes Q1 → Q3. | **`time_on_materials_min_q3 - time_on_materials_min_q1`** |
| `total_logins` | Float | Sum of quarterly logins. | **`logins_q1 + logins_q2 + logins_q3`** |
| `total_time` | Float | Sum of quarterly minutes on materials. | **`time_on_materials_min_q1 + time_on_materials_min_q2 + time_on_materials_min_q3`** |
| `total_forum_posts` | Float | Sum of quarterly forum posts. | **`forum_posts_q1 + forum_posts_q2 + forum_posts_q3`** |
| `is_ghost` | Integer (0/1) | No LMS logins across Q1–Q3 (after fill). | **`1` if `total_logins == 0`, else `0`**. |
| `early_engagement_academic_friction` | Float | Interaction: credit-failure risk relative to **early** (Q1) engagement. Higher = higher risk + lower early logins. | **`credits_failed_pct / (logins_q1 + 1)`** |
| `total_login_academic_friction` | Float | Interaction: credit-failure risk relative to **total** engagement (logins). Higher = higher risk + lower total logins. | **`credits_failed_pct / (total_logins + 1)`** |
| `total_time_academic_friction` | Float | Interaction: credit-failure risk relative to **total** engagement (time on materials). Higher = higher risk + lower total time. | **`credits_failed_pct / (total_time + 1)`** |

---

## Wide engagement features (how they are built)

1. Long-form engagement: `student_id`, `quarter` ∈ {Q1, Q2, Q3}, `logins`, `time_on_materials_min`, `forum_posts`.
2. **Pivot:** index `student_id`, columns `quarter`, values the three metrics; flattened names `metric_q*` (e.g. `logins_q1`).
3. **Left merge** onto cleaned registry on `student_id`.
4. Columns whose names contain **`_q`** get **`.fillna(0)`** so every registry student has numeric engagement (zeros = no observed LMS activity).

---

## Exclusions and data quality rules (registry)

- **Major:** CS label harmonization.
- **Age:** `-1` → missing; median by `major`.
- **prior_gpa:** outside \[0, 4\] → missing; median by `major`.
- **financial_aid:** complete-case deletion (null aid removed).

---

## File location

- **Dataset and dictionary** live under **`data/`** so schema and artifact stay together.
- **Notebook export:** `01_Wrangling_Exploration.ipynb` writes the cleaned features CSV to **`data_dir / "student_registry_cleaned_features.csv"`** (run the data-loading cell first so `data_dir` exists).

---

*Aligned with `01_Wrangling_Exploration.ipynb` and synthetic-data assumptions confirmed by the project author.*
