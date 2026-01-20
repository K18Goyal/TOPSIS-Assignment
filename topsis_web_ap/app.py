import streamlit as st
import pandas as pd
import numpy as np
import re
import smtplib
from email.message import EmailMessage

# ------------------ Helper Functions ------------------

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def topsis(df, weights, impacts):
    data = df.copy()
    numeric = data.iloc[:, 1:].apply(pd.to_numeric)

    # Normalize
    norm = np.sqrt((numeric ** 2).sum())
    normalized = numeric / norm

    # Apply weights
    weighted = normalized * weights

    # Ideal best & worst
    ideal_best, ideal_worst = [], []

    for i in range(len(weights)):
        if impacts[i] == "+":
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Distances
    d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)

    data["Topsis Score"] = score
    data["Rank"] = data["Topsis Score"].rank(
        ascending=False, method="dense"
    ).astype(int)

    return data

def send_email(receiver, csv_text):
    if "EMAIL" not in st.secrets or "PASSWORD" not in st.secrets:
        return False

    sender = st.secrets["EMAIL"]
    password = st.secrets["PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Please find attached the TOPSIS result file.")

    msg.add_attachment(csv_text, filename="topsis_result.csv")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    return True

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="TOPSIS Web App")
st.title("TOPSIS Web Application")

st.write("Upload CSV file, enter weights & impacts. Result will be shown and downloadable.")
st.write("Email is optional.")

file = st.file_uploader("Upload CSV File", type=["csv"])
weights = st.text_input("Enter Weights (comma separated)", "1,1,1,1")
impacts = st.text_input("Enter Impacts (+ or -, comma separated)", "+,+,+,+")
email = st.text_input("Enter Email (optional)")

if st.button("Submit"):
    if not file:
        st.error("Please upload a CSV file.")
        st.stop()

    try:
        df = pd.read_csv(file)

        if df.shape[1] < 3:
            st.error("CSV must have at least 1 name column + 2 criteria.")
            st.stop()

        w = list(map(float, weights.split(",")))
        i = impacts.split(",")

        if len(w) != len(i) or len(w) != df.shape[1] - 1:
            st.error("Weights, impacts and criteria count must match.")
            st.stop()

        for x in i:
            if x not in ["+", "-"]:
                st.error("Impacts must be + or - only.")
                st.stop()

        result = topsis(df, np.array(w), i)
        csv_text = result.to_csv(index=False)

        st.success("TOPSIS calculation successful!")
        st.dataframe(result)

        st.download_button(
            "Download Result CSV",
            csv_text,
            file_name="topsis_result.csv",
            mime="text/csv"
        )

        if email:
            if not is_valid_email(email):
                st.warning("Invalid email format. Skipping email.")
            else:
                sent = send_email(email, csv_text)
                if sent:
                    st.success("Result sent to email successfully!")
                else:
                    st.info("Email service not configured. Download instead.")

    except Exception as e:
        st.error(str(e))
