import streamlit as st
import pandas as pd
import numpy as np
import re
import smtplib
from email.message import EmailMessage

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def topsis(df, weights, impacts):
    data = df.copy()
    numeric = data.iloc[:, 1:].apply(pd.to_numeric)

    norm = np.sqrt((numeric ** 2).sum())
    normalized = numeric / norm
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(weights)):
        if impacts[i] == "+":
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data["Topsis Score"] = score
    data["Rank"] = data["Topsis Score"].rank(ascending=False, method="dense").astype(int)

    return data

def send_email(receiver, csv_text):
    sender = st.secrets["EMAIL"]
    password = st.secrets["PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Please find attached the TOPSIS result file.")

    msg.add_attachment(
        csv_text.encode(),
        maintype="text",
        subtype="csv",
        filename="topsis_result.csv"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

st.title("TOPSIS Web Application!")
st.write("Upload CSV, enter Weights, Impacts and Email")

file = st.file_uploader("Upload CSV File", type=["csv"])
weights = st.text_input("Enter Weights (comma separated)")
impacts = st.text_input("Enter Impacts (comma separated, + or -)")
email = st.text_input("Enter Email")

if st.button("Submit"):
    if not file:
        st.error("Please upload a CSV file.")
    elif not weights or not impacts:
        st.error("Weights and impacts are required.")
    else:
        try:
            df = pd.read_csv(file)
            w = list(map(float, weights.split(",")))
            i = impacts.split(",")

            result = topsis(df, np.array(w), i)
            csv_text = result.to_csv(index=False)

            st.success("TOPSIS calculated successfully!")
            st.dataframe(result)

            # ✅ DOWNLOAD OPTION (ALWAYS AVAILABLE)
            st.download_button(
                label="⬇ Download Result CSV",
                data=csv_text,
                file_name="topsis_result.csv",
                mime="text/csv"
            )

            # ✅ EMAIL OPTION (OPTIONAL)
            if email and is_valid_email(email):
                try:
                    send_email(email, csv_text)
                    st.success("Result sent to email successfully!")
                except:
                    st.warning("Email failed. Please download the result.")

        except Exception as e:
            st.error(str(e))
