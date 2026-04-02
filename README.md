# Student Dropout Prediction using Machine Learning

## Problem

Student dropout is a major challenge for educational institutions, both financially and in terms of student outcomes. The goal of this project was to build a model that can identify students at risk of dropping out early, so that support can be provided before it’s too late.

## Approach

Created a synthetic dataset (~7,500 students) to simulate demographic information, prior academic performance, and LMS engagement data  
Explored the data to understand patterns between engagement, performance, and dropout  
Built features combining academic history and behavioral signals (e.g. activity levels, prior gpa)  
Trained and compared Logistic Regression and XGBoost models  
Focused on improving recall, to make sure at-risk students are not missed  


## Results
Recall: 85% (able to identify most at-risk students)  
Precision: 83%  
The dataset was imbalanced, with dropout representing a minority class  
The model captured clear patterns between disengagement, academic history and dropout risk  


## Key Insights
Lower engagement (e.g. logins, time spent of materials) is strongly linked to dropout  
Academic performance alone isn’t enough to identify at-risk students  
Combining behavioural and academic data gives a much clearer signal  


## Tech Stack
Python, Pandas, Scikit-learn, XGBoost, Matplotlib, Seaborn

## Next Steps
Currently, the model is designed to run at the end of Q3. For future iterations, I plan to experiment using only engagement data from Q1 and Q2. This will allow me to measure the trade-off between model recall and intervention timing. Finding a viable predictive signal after Q2 would provide schools more time to intervene.













