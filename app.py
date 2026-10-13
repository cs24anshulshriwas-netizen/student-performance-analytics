
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Analytics")
st.write("Analyze student marks and attendance in one place.")

# Subjects from your timetable
subjects = [
    "TOC",
    "DBMS",
    "Data Analytics",
    "IWT",
    "Soft Skills",
    "Linux",
    "Python",
    "Writing School"
]

st.subheader("📂 Upload Student Data")

uploaded_file = st.file_uploader(
    "Upload student data (CSV)",
    type=["csv"]
)

required_columns = ["Name"] + subjects + ["Attendance"]

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if all(column in df.columns for column in required_columns):
            df = df[required_columns].copy()

            for column in subjects + ["Attendance"]:
                df[column] = pd.to_numeric(
                    df[column], errors="coerce"
                )

            df = df.dropna(subset=required_columns)

            if df.empty:
                st.error("CSV has no valid student records.")
                st.stop()

            st.success("CSV uploaded successfully!")

        else:
            st.error(
                "CSV must contain: Name, "
                + ", ".join(subjects)
                + ", Attendance"
            )
            st.stop()

    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()

else:
    data = {
        "Name": ["Rahul", "Priya", "Aman", "Sneha", "Karan"],
        "TOC": [85, 92, 45, 76, 65],
        "DBMS": [78, 88, 52, 80, 70],
        "Data Analytics": [82, 85, 48, 74, 68],
        "IWT": [80, 90, 50, 78, 72],
        "Soft Skills": [88, 91, 60, 82, 75],
        "Linux": [76, 84, 42, 73, 66],
        "Python": [90, 95, 55, 85, 74],
        "Writing School": [86, 89, 58, 80, 71],
        "Attendance": [92, 95, 68, 88, 82]
    }

    df = pd.DataFrame(data)

# Calculate average and result
df["Average Marks"] = df[subjects].mean(axis=1)

df["Result"] = df["Average Marks"].apply(
    lambda marks: "Pass" if marks >= 40 else "Fail"
)

def get_category(marks):
    if marks >= 80:
        return "Excellent"
    elif marks >= 60:
        return "Good"
    elif marks >= 40:
        return "Average"
    else:
        return "Needs Improvement"

df["Performance"] = df["Average Marks"].apply(get_category)

# Dashboard
st.subheader("📊 Dashboard Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(df))
col2.metric(
    "Average Marks",
    round(df["Average Marks"].mean(), 2)
)
col3.metric(
    "Average Attendance",
    f"{df['Attendance'].mean():.1f}%"
)

col4, col5 = st.columns(2)

col4.metric(
    "Students Passed",
    (df["Result"] == "Pass").sum()
)
col5.metric(
    "Students Failed",
    (df["Result"] == "Fail").sum()
)

# Subject-wise chart
st.subheader("📈 Subject-wise Performance")

chart_data = df[subjects].mean().reset_index()
chart_data.columns = ["Subject", "Average Marks"]

fig = px.bar(
    chart_data,
    x="Subject",
    y="Average Marks",
    title="Average Marks by Subject",
    color="Subject"
)

st.plotly_chart(fig, width="stretch")

# Attendance alerts
st.subheader("🚨 Low Attendance Alerts")

low_attendance = df[df["Attendance"] < 75]

if not low_attendance.empty:
    st.warning(
        f"{len(low_attendance)} student(s) have attendance below 75%."
    )
    st.dataframe(
        low_attendance[["Name", "Attendance"]],
        width="stretch"
    )
else:
    st.success("All students have attendance of 75% or above!")

# Search and filters
st.subheader("🔎 Search and Filter Students")

col1, col2 = st.columns(2)

with col1:
    search_name = st.text_input("Search student by name")

with col2:
    result_filter = st.selectbox(
        "Filter by result",
        ["All", "Pass", "Fail"]
    )

filtered_df = df.copy()

if search_name:
    filtered_df = filtered_df[
        filtered_df["Name"].astype(str).str.contains(
            search_name, case=False, na=False
        )
    ]

if result_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Result"] == result_filter
    ]

# Student records
st.subheader("📋 Student Records")
st.dataframe(filtered_df, width="stretch")

st.caption(f"Showing {len(filtered_df)} student(s)")

# Download report
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Student Report",
    data=csv_data,
    file_name="student_performance_report.csv",
    mime="text/csv"
)
