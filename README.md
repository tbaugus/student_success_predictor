# Student Dropout Prediction using Machine Learning

## Problem

Educational institutions struggle to identify at-risk students before they drop out, leading to lost tuition revenue and diminished student success metrics. The goal of this project was to build a predictive model that uses student engagement data measured quarterly (Q1-Q3) and demographic information to identify students at risk of dropping out, enabling the Student Success Team to deploy targeted interventions during the final term to improve success rates.

## Approach

Created a synthetic dataset (~7,500 students) to simulate demographic information, prior academic performance, and LMS engagement data  
Explored the data to understand patterns between engagement, performance, and dropout  
Built features combining academic history and behavioral signals (e.g. activity levels, prior gpa)  
Trained and compared Logistic Regression and XGBoost models  
Focused on improving recall, to make sure at-risk students are not missed  


## Results- 
XGBoost model chosen to balance precision and recall
Recall: 85% (able to identify most at-risk students)  
Precision: 83%
Linear Regression option if resources are available
Recall: 94% (identifies almost every at-risk student)
Precision: 73% 
The dataset was imbalanced, with dropout representing a minority class  
The model captured clear patterns between disengagement, academic history and dropout risk

## Feature Importance
Inputs are ranked by mean absolute SHAP* impact on predicted dropout risk, grouping one-hot columns back to the original variable (e.g. major, gender). The variables with the largest average influence on dropout predictions were:
1. credits_failed_pct - classes failed ÷ all classes taken over the college career
2. total_time_academic_friction - Interaction: credit-failure risk relative to total engagement (time on materials)
3. prior_gpa - Prior cumulative GPA (0–4 scale)
4. total_login_academic_friction - Interaction: credit-failure risk relative to total engagement (logins)
5. total_time - Sum of quarterly minutes on materials
Conclusion: These variables all fall into two larger groups: prior academic performance and engagement frequency/duration
* Method: TreeExplainer (XGBoost, preprocessed features); background = up to 200 random training rows; explained set = 800 test rows; importance = mean |SHAP|, grouped by summing one-hots per variable. Listed features are the top five.

## Key Insights
Lower engagement (e.g. logins, time spent on materials) is strongly linked to dropout  
Academic performance alone isn’t enough to identify at-risk students 
"Ghost" students are at a much higher risk for dropping out 
Combining behavioral and academic data gives a much clearer signal  


## Tech Stack
Python, Pandas, Scikit-learn, XGBoost, SHAP, Matplotlib, Seaborn

## Next Steps
Currently, the model is designed to run at the end of Q3. For future iterations, I plan to experiment using only engagement data from Q1 and Q2. This will allow me to measure the trade-off between model recall and intervention timing. Finding a viable predictive signal after Q2 would provide schools more time to intervene. I would also experiment using real-world data to determine signal strength on realistic variations.













