import pandas as pd
import numpy as np
import streamlit as st 
import plotly.express as px

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
        return df[df["Biblical Content"] == user_selected_book]

    

column_types = {"Manuscript": "string", "Folio": "string", "Column": "int64", "Line": "int64", "Words": "float64", "Biblical Content": "string", "Corrections": "int64", "Nomina Sacra": "int64" }
df = pd.read_csv("mss_data/gpp_mss_stats2.csv", dtype=column_types)

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

if len(user_selected_biblical_content_df) != 0:
    total_folios = len(user_selected_biblical_content_df["Folio"].unique())
    total_words = user_selected_biblical_content_df["Words"].sum()
    total_lines = user_selected_biblical_content_df.shape[0]
    average_words_per_folio = round(total_words / total_folios, 2)
    average_lines_per_folio = round(total_lines / total_folios, 2)
    average_words_per_line = round(total_words / total_lines, 2)
    average_letter_per_line = round(user_selected_biblical_content_df["Letters"].mean(), 2)
    average_syllables_per_line = round(user_selected_biblical_content_df["Syllables"].mean(), 2)
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
    mss_info_c2.write(f"Average Number of Letters Per Line: {average_letter_per_line}")
    mss_info_c2.write(f"Average Number of Syllables Per Line: {average_syllables_per_line}")
    mss_info_c2.write(f"Total Number of Corrections: {total_corrections}")
    mss_info_c2.write(f"Total Number of Nomina Sacra: {total_nomina_sacra}")

st.header("Folio Totals Bar Charts")

folio_line_totals = user_selected_biblical_content_df.groupby("Folio")["Line"].count().reset_index()
folio_word_totals = user_selected_biblical_content_df.groupby("Folio")["Words"].sum().reset_index()
folio_letter_totals = user_selected_biblical_content_df.groupby("Folio")["Letters"].sum().reset_index()
folio_syllable_totals = user_selected_biblical_content_df.groupby("Folio")["Syllables"].sum().reset_index()
folio_correction_totals = user_selected_biblical_content_df.groupby("Folio")["Corrections"].sum().reset_index()
folio_nomina_sacra_totals = user_selected_biblical_content_df.groupby("Folio")["Nomina Sacra"].sum().reset_index()

lines_folio_fig = px.histogram(folio_line_totals, x="Line", y="Folio")
words_folio_fig = px.histogram(folio_word_totals, x="Words", y="Folio")
letters_folio_fig = px.histogram(folio_letter_totals, x="Letters", y="Folio")
syllables_folio_fig = px.histogram(folio_syllable_totals, x="Syllables", y="Folio")
corrections_folio_fig = px.histogram(folio_correction_totals, x="Corrections", y="Folio")
nomina_sacra_folio_fig = px.histogram(folio_nomina_sacra_totals, x="Nomina Sacra", y="Folio")

chart_tab1, chart_tab2, chart_tab3, chart_tab4, chart_tab5, chart_tab6 = st.tabs(["Lines Per Folio", "Words Per Folio", "Letters Per Folio", "Syllables Per Folio", "Corrections Per Folio", "Nomina Sacra Per Folio"])
with chart_tab1:
    st.plotly_chart(lines_folio_fig)

with chart_tab2:
    st.plotly_chart(words_folio_fig)

with chart_tab3:
    st.plotly_chart(letters_folio_fig)

with chart_tab4:
    st.plotly_chart(syllables_folio_fig)

with chart_tab5:
    st.plotly_chart(corrections_folio_fig)

with chart_tab6:
    st.plotly_chart(nomina_sacra_folio_fig)

st.header("Words Per Line")

unique_folios = user_selected_biblical_content_df["Folio"].unique()
tabs = st.tabs(unique_folios)
for i, tab in enumerate(tabs):
    with tab:
        folio_df = user_selected_biblical_content_df[user_selected_biblical_content_df["Folio"] == unique_folios[i]]
        small_df = folio_df.loc[:, ['Line', 'Words', "Column"]].reset_index(drop=True)
        num_of_columns = small_df["Column"].max()
        if num_of_columns > 1:
            unique_columns = small_df["Column"].unique()
            for i, column in enumerate(unique_columns):
                column_df = small_df[small_df["Column"] == unique_columns[i]]
                st.subheader(f"Column: {unique_columns[i]}")
                st.bar_chart(column_df, x="Line", y="Words")
        else:
            st.bar_chart(small_df, x="Line", y="Words")

st.header("Letters Per Line")

unique_folios = user_selected_biblical_content_df["Folio"].unique()
tabs = st.tabs(unique_folios)
for i, tab in enumerate(tabs):
    with tab:
        folio_df = user_selected_biblical_content_df[user_selected_biblical_content_df["Folio"] == unique_folios[i]]
        small_df = folio_df.loc[:, ['Line', 'Letters', "Column"]].reset_index(drop=True)
        num_of_columns = small_df["Column"].max()
        if num_of_columns > 1:
            unique_columns = small_df["Column"].unique()
            for i, column in enumerate(unique_columns):
                column_df = small_df[small_df["Column"] == unique_columns[i]]
                st.subheader(f"Column: {unique_columns[i]}")
                st.bar_chart(column_df, x="Line", y="Letters")
        else:
            st.bar_chart(small_df, x="Line", y="Letters")

st.header("Syllables Per Line")

unique_folios = user_selected_biblical_content_df["Folio"].unique()
tabs = st.tabs(unique_folios)
for i, tab in enumerate(tabs):
    with tab:
        folio_df = user_selected_biblical_content_df[user_selected_biblical_content_df["Folio"] == unique_folios[i]]
        small_df = folio_df.loc[:, ['Line', 'Syllables', "Column"]].reset_index(drop=True)
        num_of_columns = small_df["Column"].max()
        if num_of_columns > 1:
            unique_columns = small_df["Column"].unique()
            for i, column in enumerate(unique_columns):
                column_df = small_df[small_df["Column"] == unique_columns[i]]
                st.subheader(f"Column: {unique_columns[i]}")
                st.bar_chart(column_df, x="Line", y="Syllables")
        else:
            st.bar_chart(small_df, x="Line", y="Syllables")

st.header("Corrections Per Line")

unique_folios = user_selected_biblical_content_df["Folio"].unique()
tabs = st.tabs(unique_folios)
for i, tab in enumerate(tabs):
    with tab:
        folio_df = user_selected_biblical_content_df[user_selected_biblical_content_df["Folio"] == unique_folios[i]]
        small_df = folio_df.loc[:, ['Line', 'Corrections', "Column"]].reset_index(drop=True)
        num_of_columns = small_df["Column"].max()
        if num_of_columns > 1:
            unique_columns = small_df["Column"].unique()
            for i, column in enumerate(unique_columns):
                column_df = small_df[small_df["Column"] == unique_columns[i]]
                st.subheader(f"Column: {unique_columns[i]}")
                st.bar_chart(column_df, x="Line", y="Corrections")
        else:
            st.bar_chart(small_df, x="Line", y="Corrections")

st.header("Nomina Sacra Per Line")

unique_folios = user_selected_biblical_content_df["Folio"].unique()
tabs = st.tabs(unique_folios)
for i, tab in enumerate(tabs):
    with tab:
        folio_df = user_selected_biblical_content_df[user_selected_biblical_content_df["Folio"] == unique_folios[i]]
        small_df = folio_df.loc[:, ['Line', 'Nomina Sacra', "Column"]].reset_index(drop=True)
        num_of_columns = small_df["Column"].max()
        if num_of_columns > 1:
            unique_columns = small_df["Column"].unique()
            for i, column in enumerate(unique_columns):
                column_df = small_df[small_df["Column"] == unique_columns[i]]
                st.subheader(f"Column: {unique_columns[i]}")
                st.bar_chart(column_df, x="Line", y="Nomina Sacra")
        else:
            st.bar_chart(small_df, x="Line", y="Nomina Sacra")
