# 🏎️ The Speed Myth: 75 Years of F1 Data Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🏁 Overview
This project is an interactive data documentary built for the **Codédex Data Science / Data Analysis Monthly Challenge**. 
It explores 75 years of Formula 1 historical data (sourced from Kaggle) to answer one specific question: *In a sport obsessed with speed, does having the fastest car actually guarantee a World Championship?*

## 💡 The Findings
Through extensive data wrangling and visualization, this dashboard uncovers:
* **The 80% Rule:** The fastest car wins the championship roughly 77.3% of the time. Raw speed is the baseline, but not a guarantee.
* **The "Death of the DNF":** A massive shift in F1 history occurred around the year 2000. Before then, mechanical failures ("Did Not Finish") created a chaotic survival lottery. Today, bulletproof reliability makes upsets incredibly rare.
* **Teammate Suppression Index (TSI):** A custom metric designed to isolate driver skill by comparing legends strictly against the only other person on the grid in the exact same machinery.

## 🛠️ Tech Stack
* **Data Wrangling:** `pandas`
* **Web Framework:** `streamlit` (with custom CSS for dark-mode UI)
* **Interactive Visualization:** `plotly.express`, `plotly.graph_objects`

## 🚀 How to Run Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/Vivek1625/f1-75-years-analysis.git](https://github.com/Vivek1625/f1-75-years-analysis.git)
