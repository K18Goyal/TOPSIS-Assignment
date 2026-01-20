import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TOPSIS Web App")

st.title("TOPSIS Web Service")

st.write("Upload CSV file, enter weights & impacts")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

weights = st.text_input("Enter Weights (comma separated)", "1,1,1,1")
impacts = st.text_input("Enter Impacts (+ or - comma separated)", "+,+,+,+")
email = st.text_input("Enter Email ID")

def topsis(df, weights, impacts):
    data = df.iloc[:, 1:].values.astype(float)

    norm = np.sqrt((data**2).sum(axis=0))
    data = data / norm
    data = data * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(data[:, i].max())
            ideal_worst.append(data[:, i].min())
        else:
            ideal_best.append(data[:, i].min())
            ideal_worst.append(data[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    d_best = np.sqrt(((data - ideal_best)**2).sum(axis=1))
    d_worst = np.sqrt(((data - ideal_worst)**2).sum(axis=1))

    score = d_worst / (d_best + d_worst)
    rank = score.argsort()[::-1] + 1

    df["Topsis Score"] = score
    df["Rank"] = rank
    return df

if st.button("Submit"):
    if uploaded_file is None:
        st.error("Please upload a CSV file")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            w = list(map(float, weights.split(",")))
            imp = impacts.split(",")

            if len(w) != len(imp):
                st.error("Weights and impacts count must be same")
            else:
                result = topsis(df, np.array(w), imp)
                st.success("TOPSIS Calculated Successfully")
                st.dataframe(result)

                result.to_csv("result.csv", index=False)

                st.download_button(
                    "Download Result CSV",
                    result.to_csv(index=False),
                    "result.csv",
                    "text/csv"
                )
        except Exception as e:
            st.error(str(e))
