import pandas as pd
import numpy as np
import streamlit as st 

# Functions
def word_diff(mss_total_words: int, na28_total_words: int):
    difference = mss_total_words - na28_total_words
    if difference > 0:
        return f"{difference} words more than NA28."
    elif difference == 0:
        return "Same amount of words."
    else:
        return f"{abs(difference)} words less than NA28."

def user_selected_df(user_selected_book:str, df:pd.DataFrame):
    if user_selected_book == "1Tim-Titus":
        return df
    else:
        user_selected_book_df = df[df["Biblical Content"] == user_selected_book]
        return user_selected_book_df

    

column_types = {"Manuscript": "string", "Folio": "string", "Column": "int64", "Line": "int64", "Words": "float64", "Biblical Content": "string", "Corrections": "int64", "Nomina Sacra": "int64" }
df = pd.read_csv("mss_data/gpp_mss_stats.csv", dtype=column_types)

na28_word_count = {
    "1Tim-Titus": 3496,
    "1Tim": 1594,
    "2Tim": 1241,
    "Titus": 661
}

st.title("Greek Paul Project MSS Statistical Information")
mss_selection = st.selectbox(
    "Which manuscript would you like to explore?",
    df["Manuscript"].unique()
)
book_selection = st.selectbox(
    "Which book(s) would you like to view statistics for?",
    ["1Tim-Titus", "1Tim", "2Tim", "Titus"]
)
# Stats for Mss User Selected
user_selected_mss_df = df[df["Manuscript"] == mss_selection]
user_selected_biblical_content_df = user_selected_df(book_selection, user_selected_mss_df)
na28_word = na28_word_count[book_selection]

if len(user_selected_biblical_content_df) == 0:
    pass
else:
    total_folios = len(user_selected_biblical_content_df["Folio"].unique())
    total_words = user_selected_biblical_content_df["Words"].sum()
    total_lines = user_selected_biblical_content_df.shape[0]
    average_words_per_folio = round(total_words / total_folios, 2)
    average_lines_per_folio = round(total_lines / total_folios, 2)
    average_words_per_line = round(total_words / total_lines, 2)
    most_columns = user_selected_biblical_content_df["Column"].max()
    total_corrections = user_selected_biblical_content_df["Corrections"].sum()
    total_nomina_sacra = user_selected_biblical_content_df["Nomina Sacra"].sum()

mss_info_container = st.container()             
mss_info_c1, mss_info_c2 = st.columns(2)
mss_info_container.header(f"Statistics for Manuscript {mss_selection} of {book_selection}")
mss_info_container.divider()
if len(user_selected_biblical_content_df) == 0:
    mss_info_container.subheader(f"{mss_selection} does not contain content from {book_selection}")
else:
    mss_info_c1.write(f"Total Number of Folios: {total_folios}")
    mss_info_c1.write(f"Total Number of Lines: {total_lines}")
    mss_info_c1.write(f"Total Number of Words: {total_words}")
    mss_info_c1.write(f"Total Number of Words in NA28: {na28_word}")
    mss_info_c1.write(f"Word difference between {mss_selection} and NA28: {word_diff(total_words, na28_word)}")
    mss_info_c1.write(f"Average Number of Lines Per Folio: {average_lines_per_folio}")
    mss_info_c2.write(f"Usual Number of Columns on a Folio: {most_columns}")
    mss_info_c2.write(f"Average Words Per Folio: {average_words_per_folio}")
    mss_info_c2.write(f"Average Number of Words Per Line: {average_words_per_line}")
    mss_info_c2.write(f"Total Number of Corrections: {total_corrections}")
    mss_info_c2.write(f"Total Number of Nomina Sacra: {total_nomina_sacra}")

st.header("Bar Charts")

chart_tab1, chart_tab2, chart_tab3 = st.tabs(["Words Per Folio", "Corrections Per Folio", "Nomina Sacra Per Folio"])
chart_tab1.write("This is tab 1")
chart_tab2.write("This is tab 2")
chart_tab3.write("This is tab 3")