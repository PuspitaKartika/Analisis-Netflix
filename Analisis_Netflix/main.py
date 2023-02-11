import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

df = pd.read_csv("netflix_titles.csv")

dfGenre = df[['show_id', 'listed_in']]
dfGenre['listed_in'] = df['listed_in'].apply(lambda x: x.split(', '))

id_list, genre_list = [], []
for index in dfGenre.index:
    id = dfGenre.at[index, 'show_id']
    genres = dfGenre.at[index, 'listed_in']
    for genre in genres:
        id_list.append(id)
        genre_list.append(genre)

dfGenre = pd.DataFrame()
dfGenre = dfGenre.assign(id=id_list, genre=genre_list)

dfCast = df[['show_id', 'cast']].loc[df['cast'].notna()]
dfCast['cast'] = dfCast['cast'].apply(lambda x: x.split(', '))

id_list, cast_list = [], []
for index in dfCast.index:
    id = dfCast.at[index, 'show_id']
    casts = dfCast.at[index, 'cast']
    for cast in casts:
        id_list.append(id)
        cast_list.append(cast)

dfCast = pd.DataFrame()
dfCast = dfCast.assign(id=id_list, cast=cast_list)

st.title("Analisis Netflix")

number = st.number_input('top number', 2)

tab1, tab2, tab3 = st.tabs(["Genre", "Artis", "Derection"])

if number != 0:
    with tab1:
        st.subheader('TOP ' + str(number) + ' Genre Netflix')
        dfPlot = dfGenre.groupby('genre').size().reset_index(
            name='size').sort_values(by='size', ascending=False).head(int(number))
        colors = sb.color_palette('coolwarm')[0:len(dfPlot)]
        plt.figure(figsize=(18, 8))

        plt.bar(dfPlot['genre'], dfPlot['size'], color=colors, width=0.8)
        for i, j in zip(dfPlot['genre'], dfPlot['size']):
            plt.annotate(str(j), xy=(i, j), fontsize=18,
                         color='black', ha='center', va='bottom')
        plt.xlabel('Genre',  fontsize=16)
        plt.ylabel('Number of genre shows',  fontsize=16)
        plt.xticks(rotation=45, fontsize=12)
        st.pyplot(plt)
    #  plt.show()

    with tab2:
        st.subheader('TOP ' + str(number) + ' Artis Netflix')
        dfPlot = dfCast.groupby('cast').size().reset_index(
            name='size').sort_values(by='size', ascending=False).head(int(number))
        colors = sb.color_palette('coolwarm')[0:len(dfPlot)]
        plt.figure(figsize=(18, 8))

        plt.bar(dfPlot['cast'], dfPlot['size'], color=colors, width=0.8)
        for i, j in zip(dfPlot['cast'], dfPlot['size']):
            plt.annotate(str(j), xy=(i, j), fontsize=18,
                         color='black', ha='center', va='bottom')
        plt.xlabel('Artis',  fontsize=16)
        plt.ylabel('Number of artis shows',  fontsize=16)
        plt.xticks(rotation=45, fontsize=12)
        st.pyplot(plt)
        # plt.show()

    with tab3:
        st.subheader('TOP ' + str(number) + ' Derection Netflix')
        dfPlot = df.groupby('director').size().reset_index(
            name='size').sort_values(by='size', ascending=False).head(int(number))
        colors = sb.color_palette('coolwarm')[0:len(dfPlot)]
        plt.figure(figsize=(18, 8))

        plt.bar(dfPlot['director'], dfPlot['size'],
                color=colors, width=0.8)

        for i, j in zip(dfPlot['director'], dfPlot['size']):
            plt.annotate(str(j), xy=(i, j), fontsize=18,
                         color='black', ha='center', va='bottom')
        plt.xlabel('Director',  fontsize=16)
        plt.ylabel('Number of directed shows',  fontsize=16)
        plt.xticks(rotation=45, fontsize=12)
        st.pyplot(plt)
        # plt.show()

# Perbandingan Movie
st.header("Perbandingan Movie & TV show")
col1, col2 = st.columns(2)
with col1:
    char_data = pd.DataFrame(
        df.type.value_counts()
    )
    st.bar_chart(char_data)

with col2:
    dfPlot = df.groupby('type').size().reset_index(
        name='size').sort_values(by='size', ascending=False)
    colors = sb.color_palette('coolwarm')[0:len(dfPlot)]
    plt.pie(dfPlot['size'], colors=colors,
            autopct='%.0f%%', radius=3, textprops={'fontsize': 25},)
    plt.xlabel('TV Show',  fontsize=25,)
    plt.ylabel('Movie',  fontsize=25,)
    st.pyplot(plt)
    # plt.show()
    st.write(" Movie = 69%  TV Show = 31% ")

st.subheader("Negara dengan penonton terbanyak")
top_negara = st.number_input("Jumlah negara", 3)
char_data1 = pd.DataFrame(
    # Note adding color to the horizontal bars.
    df["country"].value_counts().head(top_negara),
)

genre = st.radio(
    "Pilih tampilan grafix",
    ('Line Char', 'Bar Char')
)
if genre == 'Line Char':
    st.line_chart(char_data1)
else:
    st.bar_chart(char_data1)


char_data1 = pd.DataFrame(
    # Note adding color to the horizontal bars.
    df["duration"].value_counts().head(20),
)
st.subheader("Durasi penayangan TV Show dan Movie pada Netflix")

st.bar_chart(char_data1)

# Footer
st.markdown("<t style='text-align: center; color: grey; '>Copyright © 2023</t>",
            unsafe_allow_html=True)
