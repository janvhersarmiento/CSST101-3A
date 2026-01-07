from flask import Flask, render_template, request
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

model = joblib.load("student_risk_model.pkl")

df = pd.read_csv("Final Cleaned Data.csv")

encoder = LabelEncoder()

categorical_columns = [
    'Device_Type',
    'Internet_Access',
    'Engagement_Level',
    'Teacher_Quality'
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = encoder.fit_transform(df[col].astype(str))

X = df[
    [
        "Login_Frequency",
        "Time_Spent_Modules",
        "Participation_Forums",
        "Quiz_Performance_Average",
        "Assignment_Submissions",
        "Resource_Access_Frequency",
        "Session_Duration_Average",
        "Engagement_Level",
        "Hours_Studied",
        "Attendance",
        "Device_Type",
        "Internet_Access",
        "Internet_Bandwidth",
        "Previous_Scores",
        "Sleep_Hours",
        "Tutoring_Sessions",
        "Physical_Activity",
        "Teacher_Quality",
    ]
]

df["Predicted_Risk"] = model.predict(X)

def apply_krr(row):
    if row["Attendance"] < 60 and row["Engagement_Level"] <= 1:
        return "High"
    elif row["Attendance"] > 90 and row["Engagement_Level"] >= 3:
        return "Low"
    else:
        return row["Predicted_Risk"]

df["Final_Risk"] = df.apply(apply_krr, axis=1)

risk_counts = (
    df["Final_Risk"]
    .value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
    .to_dict()
)

if not os.path.exists("static"):
    os.makedirs("static")

def generate_dashboard_chart():
    plt.figure(figsize=(6, 4))
    plt.plot(
        ["Low", "Moderate", "High"],
        [risk_counts["Low"], risk_counts["Moderate"], risk_counts["High"]],
        marker="o",
        color='b'
    )
    plt.title("Student Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Students")
    plt.grid(True)
    plt.savefig("static/risk_dashboard.png")
    plt.close()

generate_dashboard_chart()

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            attendance = float(request.form["attendance"])
            quiz = float(request.form["quiz"])
            engagement_input = int(request.form["engagement"])

            features = [
                0,
                0,
                0,
                quiz,
                0,
                0,
                0,
                engagement_input,
                0,
                attendance,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]

            ml_pred = model.predict([features])[0]

            if attendance < 60 and engagement_input <= 1:
                prediction = "High"
            elif attendance > 90 and quiz >= 85:
                prediction = "Low"
            else:
                prediction = ml_pred
        
        except ValueError:
            prediction = "Error: Please enter valid numbers."

    return render_template(
        "index.html",
        prediction=prediction,
        dashboard_image="risk_dashboard.png",
        risk_counts=risk_counts
    )

if __name__ == "__main__":
    app.run(debug=True)