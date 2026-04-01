# Student Attrition and Retention Predictive Analysis

## Executive Summary
TThis project addresses the critical challenge educational institutions face in identifying at-risk students before they drop out. Utilizing a dataset synthesized to simulate actual institutional databases, this study implements a predictive model using both student demographic data and quarterly Learning Management System (LMS) engagement metrics.After evaluating multiple machine learning techniques, an XGBoost classifier was selected for its high performance. The primary goal was to build a highly sensitive early-warning system capable of identifying any student at risk of attrition. The final model achieved this goal by successfully capturing 85% of all actual dropouts across the general student population. Notably, the model maintained an exceptional 98.2% recall rate on identified "ghost" students (those with no digital trace), proving that high-risk students can still be accurately identified even when they leave no digital footprint.

---

## Introduction
Educational institutions lose substantial tuition revenue and fail to achieve target success metrics when students drop out unexpectedly. Proactive identifying markers are frequently buried in massive amounts of system data. 

The main purpose of this project is to build a high-recall machine learning model to detect attrition risks ahead of time to allow for interventions. The data used consists of a synthetic compilation of student logs and academic backgrounds, intentionally created via Gemini to simulate actual institutional database structures.

---

## Methodology

### Data Context
* **Data Sources:** The analysis relies on two compiled structures: a student registry (demographics and fixed academic history) and granular quarterly engagement statistics (time on material, logins, forum posts).
* **Unit of Observation:** Each observation in the final merged training set represents an individual student and their longitudinal activity through the first three terms of enrollment.

### Data Handling
* **Cleaning & Preparation:** Basic string columns (e.g., inconsistencies in major names like "CompSci" vs "Computer Science") were unified. Missing values in financial aid were dropped. Sentinel and missing values were handled.
* **Aggregation:** Quarterly logs were aggregated to provide features documenting trend analysis or sum totals of digital footprint sizes before fitting the models.

### Models and Analytical Techniques
1. **Exploratory Statistical Testing:** Classical Welch’s t-tests were deployed during initial exploratory data analysis to evaluate differences in baseline continuous distributions among subsets (e.g., testing academic capability between ghosts and active users).
2. **Baseline Evaluation:** A Dummy Classifier was used to establish a baseline accuracy of 85%, ensuring that class imbalance didn't create a false sense of model success. 
3. **Predictive Classifiers:** Tested both a baseline Logistic Regression model and an XGBoost classifier, utilizing class weights (scale_pos_weight and class_weight='balanced') to account for the minority dropout class.

### Assumptions
* A direct lack of LMS activity ("ghosts") acts as a heavy indicator of overall school disengagement, not technical difficulties or independent external studying outside the platform.
* Financial or academic registry entries logged at the beginning of the student's lifecycle maintain static weight throughout the observed quarters.

---

## Results & Data Analysis

### The Academic Profile of "Ghosts"
To determine if digital disengagement correlates directly with pre-existing poor academic struggle, a subset analysis evaluated "ghost" students against active digital participants. 
* Statistically, the groups are highly comparable. No significant difference was found between continuous features like Prior GPA or percentage of failed credits. 
* Both p-values from the Welch’s t-tests sat safely above 0.05, establishing that digital disengagement isn't a proxy for a lack of foundational capability or previous failure.

### Model Performance and "The Ghost Paradox"
While classical models were generated, targeted focus turned to sub-segment predictions directly on the 63 extreme disengaged "ghost" students appearing in the test matrix:
* **Ghost Recall:** 98.2%
* **Ghost Precision:** 88.7%
* **Confusion Matrix Outcomes:** True Positives (55), False Positives (7), False Negatives (1).

This distribution highlights a fascinating paradox. Even though they look academically identical to non-ghosts on intake paperwork, **88.9%** of students who stopped interacting with the LMS went on to drop out. The model accurately captured 55 out of 56 potential losses.

### Project Limitations
* **Synthetic Bias:** Because data points were programmatically generated to simulate institutional environments, natural human deviations from edge cases may not strictly reflect raw student behaviors found in production systems.

---

## Conclusion
This workflow heavily establishes that digital disengagement measured early in an academic life cycle is one of the strongest behavioral indicators of ultimate dropout risk, completely independent of past academic success. 

### Recommendations
1. **Targeting Outreach Over Remediation:** Since ghosts do not show historical academic deficiencies, counselors should not focus heavily on classic tutoring pipelines for this specific segment. Instead, outreach should focus heavily on motivational check-ins and re-engagement pathways.
2. **Automated Interventions:** Deploy automated success team campaigns centered directly on the absence of activity triggers highlighted via the XGBoost model arrays.

































# Student Retention & Attrition Predictor

## Executive Summary
This project delivers an end-to-end machine learning pipeline designed to predict student dropout risk for an educational institution. Leveraging a synthetic relational dataset of 7,500 records simulating complex, real-world data imperfections, the system identifies at-risk students using early-term behavioral engagement and financial indicators. 

By prioritizing proactive intervention, the final model successfully achieved a **78% Recall** and **82% Precision** for the minority "Dropped Out" class. This allows student success teams to accurately flag more than three-quarters of at-risk students before the final term begins, with a very low false-alarm rate.

## Key Highlights & Methodologies
* **Data Synthesis & Relational Architecture:** Modeled a multi-table schema bridging student demographics with time-series quarterly LMS engagement logs.
* **Iterative Feature Engineering:** Engineered custom interaction features (e.g., `login_academic_friction`) that captured the compound risk of low digital engagement combined with high credit failure rates, boosting recall by 4%.
* **Advanced Modeling & Optimization:** Evaluated a baseline Logistic Regression model against a fine-tuned XGBoost classifier. Utilized custom Scikit-Learn scorers in a grid search to prioritize minority class recall without sacrificing precision.
* **Analytical Maturity (The "Synthetic Data Ceiling"):** Documented the mathematical limits of a uniformly distributed synthetic dataset, proving that balanced categorical splits (e.g., equal distribution in tuition status) created a natural threshold for the model's recall capacity.







