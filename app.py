import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(
    page_title="Netflix Data Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)



@st.cache_data
def load_data():

    file_path = "output/netflix_cleaned.csv"

    if not os.path.exists(file_path):
        return None

    data = pd.read_csv(file_path)

    # Make sure duration_num is numeric
    if "duration_num" in data.columns:
        data["duration_num"] = pd.to_numeric(
            data["duration_num"],
            errors="coerce"
        )

    return data


df = load_data()



if df is None:

    st.error(
        "Cleaned dataset not found!"
    )

    st.info(
        "Please run 'python analysis.py' first."
    )

    st.stop()



st.markdown("""
<style>


.stApp {
    background-color: black;
}



[data-testid="stSidebar"] {
    background-color: darkslateblue;
}

/* Sidebar text */

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: white !important;
}


/* Sidebar headings */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: white !important;
}



h1,
h2,
h3,
h4 {
    color: white !important;
}



.stApp p {
    color: white;
}



[data-testid="stTextInput"] label {
    color: white !important;
}

[data-testid="stTextInput"] input {
    background-color: white !important;
    color: black !important;
}



[data-testid="stSelectbox"] label {
    color: white !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: white !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: black !important;
}



[data-testid="stDownloadButton"] button {

    background-color: white !important;

    color: black !important;

    border: 2px solid red !important;

    border-radius: 8px !important;

    font-weight: bold !important;

    padding: 10px 20px !important;
}


[data-testid="stDownloadButton"] button * {

    color: black !important;

}


[data-testid="stDownloadButton"] button:hover {

    background-color: red !important;

}


[data-testid="stDownloadButton"] button:hover * {

    color: white !important;

}



.stButton button {

    background-color: red !important;

    color: white !important;

    border-radius: 8px !important;

    font-weight: bold !important;

}


.stButton button * {

    color: white !important;

}



.metric-card {

    background-color: darkslategray;

    padding: 15px;

    border-radius: 10px;

    text-align: center;

    color: white !important;

    border: 1px solid red;

}


.metric-card * {

    color: white !important;

}



[data-testid="stMetricLabel"] {

    color: lightgray !important;

}


[data-testid="stMetricValue"] {

    color: cyan !important;

    font-weight: bold !important;

}



[data-testid="stDataFrame"] {

    background-color: white !important;

}



[data-testid="stExpander"] {

    background-color: darkslategray !important;

}


</style>
""", unsafe_allow_html=True)



st.sidebar.title("🎬 Netflix Dashboard")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📄 Dataset",

        "📊 KPIs",

        "🎭 Genre Analysis",

        "🌍 Country Analysis",

        "🎬 Director Analysis",

        "⭐ Actor Analysis",

        "⭐ Rating Analysis",

        "⏱ Duration Analysis",

        "📈 Charts"


    ]

)



total_titles = len(df)


movies_count = len(
    df[df["type"] == "Movie"]
)


tvshows_count = len(
    df[df["type"] == "TV Show"]
)


countries_count = df[
    "primary_country"
].nunique()


genres_count = df[
    "primary_genre"
].nunique()


directors_count = df[
    df["director"] != "Unknown"
]["director"].nunique()



actor_series = (
    df[
        df["cast"] != "Not Available"
    ]["cast"]
    .str.split(", ")
    .explode()
    .dropna()
)

total_actors = actor_series.nunique()



movie_duration = df[
    df["type"] == "Movie"
]["duration_num"].dropna()


if len(movie_duration) > 0:

    avg_movie_duration = round(
        movie_duration.mean(),
        2
    )

else:

    avg_movie_duration = 0



tv_duration = df[
    df["type"] == "TV Show"
]["duration_num"].dropna()


if len(tv_duration) > 0:

    avg_tv_seasons = round(
        tv_duration.mean(),
        2
    )

else:

    avg_tv_seasons = 0



latest_release = df[
    "release_year"
].max()


oldest_release = df[
    "release_year"
].min()



if page == "🏠 Home":

    st.title(
        "🎬 Netflix Data Analytics Dashboard"
    )

    st.markdown(
        "### Explore Netflix content using Python, SQL and Excel"
    )

    st.markdown("---")



    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Total Titles",
        total_titles
    )


    c2.metric(
        "Movies",
        movies_count
    )


    c3.metric(
        "TV Shows",
        tvshows_count
    )


    c4.metric(
        "Countries",
        countries_count
    )


    c5, c6, c7, c8 = st.columns(4)


    c5.metric(
        "Genres",
        genres_count
    )


    c6.metric(
        "Directors",
        directors_count
    )


    c7.metric(
        "Actors",
        total_actors
    )


    c8.metric(
        "Latest Release",
        latest_release
    )


    st.markdown("---")



    chart_path = (
        "charts/chart1_movies_vs_tvshows.png"
    )


    if os.path.exists(chart_path):

        st.image(
            chart_path,
            use_container_width=True
        )

    else:

        st.warning(
            "Chart 1 not found. Please run analysis.py."
        )



elif page == "📄 Dataset":

    st.title(
        "📄 Netflix Dataset"
    )



    search = st.text_input(
        "🔍 Search Title"
    )


    filtered = df.copy()


    if search:

        filtered = filtered[
            filtered["title"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]



    col1, col2 = st.columns(2)


    with col1:

        selected_type = st.selectbox(

            "Content Type",

            [
                "All",
                "Movie",
                "TV Show"
            ]

        )


    with col2:

        years = sorted(

            df[
                "release_year"
            ]
            .dropna()
            .unique(),

            reverse=True

        )


        selected_year = st.selectbox(

            "Release Year",

            ["All"] + list(years)

        )



    if selected_type != "All":

        filtered = filtered[
            filtered["type"] == selected_type
        ]



    if selected_year != "All":

        filtered = filtered[
            filtered["release_year"]
            == selected_year
        ]


    st.write(
        f"Total Records : {len(filtered)}"
    )



    st.dataframe(

        filtered,

        use_container_width=True,

        height=600

    )



elif page == "📊 KPIs":

    st.title(
        "📊 Business KPIs"
    )



    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Total Titles",
        total_titles
    )


    c2.metric(
        "Movies",
        movies_count
    )


    c3.metric(
        "TV Shows",
        tvshows_count
    )



    c4, c5, c6 = st.columns(3)


    c4.metric(
        "Countries",
        countries_count
    )


    c5.metric(
        "Genres",
        genres_count
    )


    c6.metric(
        "Directors",
        directors_count
    )



    c7, c8, c9 = st.columns(3)


    c7.metric(
        "Actors",
        total_actors
    )


    c8.metric(
        "Average Movie Duration",
        f"{avg_movie_duration} min"
    )


    c9.metric(
        "Average TV Seasons",
        avg_tv_seasons
    )



    c10, c11 = st.columns(2)


    c10.metric(
        "Oldest Release",
        oldest_release
    )


    c11.metric(
        "Latest Release",
        latest_release
    )


    st.markdown("---")



    st.subheader(
        "Dataset Summary"
    )


    summary = pd.DataFrame({

        "Metric": [

            "Total Titles",

            "Movies",

            "TV Shows",

            "Countries",

            "Genres",

            "Directors",

            "Actors",

            "Average Movie Duration",

            "Average TV Seasons",

            "Oldest Release",

            "Latest Release"

        ],


        "Value": [

            total_titles,

            movies_count,

            tvshows_count,

            countries_count,

            genres_count,

            directors_count,

            total_actors,

            avg_movie_duration,

            avg_tv_seasons,

            oldest_release,

            latest_release

        ]

    })


    st.dataframe(

        summary,

        use_container_width=True

    )



    st.markdown("---")

    st.subheader(
        "Quick Insights"
    )


    st.success(

        f"""
        ✅ Total Movies : {movies_count}

        ✅ Total TV Shows : {tvshows_count}

        ✅ Available Countries : {countries_count}

        ✅ Available Genres : {genres_count}

        ✅ Directors : {directors_count}

        ✅ Actors : {total_actors}
        """

    )



elif page == "🎭 Genre Analysis":

    st.title(
        "🎭 Genre Analysis"
    )


    genre_data = (

        df[
            "primary_genre"
        ]
        .value_counts()
        .head(15)

    )


    st.subheader(
        "Top 15 Genres"
    )


    st.bar_chart(
        genre_data
    )


    genre_table = (

        genre_data
        .reset_index()

    )


    genre_table.columns = [
        "Genre",
        "Titles"
    ]


    st.dataframe(
        genre_table,
        use_container_width=True
    )



elif page == "🌍 Country Analysis":

    st.title(
        "🌍 Country Analysis"
    )


    country_data = (

        df[
            "primary_country"
        ]
        .value_counts()
        .head(15)

    )


    st.subheader(
        "Top 15 Countries"
    )


    st.bar_chart(
        country_data
    )


    country_table = (
        country_data
        .reset_index()
    )


    country_table.columns = [
        "Country",
        "Titles"
    ]


    st.dataframe(
        country_table,
        use_container_width=True
    )



elif page == "🎬 Director Analysis":

    st.title(
        "🎬 Director Analysis"
    )


    director_data = (

        df[
            df["director"] != "Unknown"
        ]["director"]
        .value_counts()
        .head(15)

    )


    st.subheader(
        "Top 15 Directors"
    )


    st.bar_chart(
        director_data
    )


    director_table = (
        director_data
        .reset_index()
    )


    director_table.columns = [
        "Director",
        "Titles"
    ]


    st.dataframe(
        director_table,
        use_container_width=True
    )



elif page == "⭐ Actor Analysis":

    st.title(
        "⭐ Actor Analysis"
    )


    top_actors = (

        df[
            df["cast"] != "Not Available"
        ]["cast"]

        .str.split(", ")

        .explode()

        .dropna()

        .value_counts()

        .head(20)

    )


    st.subheader(
        "Top 20 Actors"
    )


    st.bar_chart(
        top_actors
    )


    actor_table = (
        top_actors
        .reset_index()
    )


    actor_table.columns = [
        "Actor",
        "Titles"
    ]


    st.dataframe(
        actor_table,
        use_container_width=True
    )



elif page == "⭐ Rating Analysis":

    st.title(
        "⭐ Rating Analysis"
    )


    rating_data = (

        df[
            "rating"
        ]
        .value_counts()

    )


    st.subheader(
        "Ratings Distribution"
    )


    st.bar_chart(
        rating_data
    )


    rating_table = (
        rating_data
        .reset_index()
    )


    rating_table.columns = [
        "Rating",
        "Titles"
    ]


    st.dataframe(
        rating_table,
        use_container_width=True
    )



elif page == "⏱ Duration Analysis":

    st.title(
        "⏱ Duration Analysis"
    )



    st.subheader(
        "🎬 Movie Duration"
    )


    if len(movie_duration) > 0:

        st.metric(

            "Average Movie Duration",

            f"{avg_movie_duration} Minutes"

        )


        fig, ax = plt.subplots(
            figsize=(10, 5)
        )


        sns.histplot(

            movie_duration,

            bins=30,

            kde=True,

            ax=ax

        )


        ax.set_title(
            "Movie Duration Distribution"
        )


        ax.set_xlabel(
            "Duration in Minutes"
        )


        ax.set_ylabel(
            "Number of Movies"
        )


        st.pyplot(fig)


        plt.close(fig)


        st.subheader(
            "Movie Duration Statistics"
        )


        st.dataframe(

            movie_duration
            .describe()
            .to_frame(),

            use_container_width=True

        )

    else:

        st.warning(
            "Movie duration data not available."
        )



    st.subheader(
        "📺 TV Show Seasons"
    )


    if len(tv_duration) > 0:

        st.metric(

            "Average TV Show Seasons",

            avg_tv_seasons

        )


        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )


        sns.countplot(

            x=tv_duration,

            ax=ax2

        )


        ax2.set_title(
            "TV Show Seasons Distribution"
        )


        ax2.set_xlabel(
            "Number of Seasons"
        )


        ax2.set_ylabel(
            "Number of TV Shows"
        )


        st.pyplot(fig2)


        plt.close(fig2)



elif page == "📈 Charts":

    st.title(
        "📈 Netflix Charts"
    )


    chart_folder = "charts"


    chart_files = [

        "chart1_movies_vs_tvshows.png",

        "chart2_top_genres.png",

        "chart3_top_countries.png",

        "chart4_ratings.png",

        "chart5_release_trend.png",

        "chart6_content_added.png",

        "chart7_directors.png",

        "chart8_actors.png",

        "chart9_movie_duration.png",

        "chart10_tvshow_seasons.png",

        "chart11_decade_distribution.png",

        "chart12_content_age.png",

        "chart13_movies_per_year.png",

        "chart14_tvshows_per_year.png",

        "chart15_top_release_years.png",

        "chart16_genre_pie.png",

        "chart17_country_pie.png",

        "chart18_boxplot.png",

        "chart19_heatmap.png",

        "chart20_missing_values.png"

    ]


    for chart in chart_files:

        path = os.path.join(
            chart_folder,
            chart
        )


        if os.path.exists(path):

            st.image(

                path,

                caption=(
                    chart
                    .replace(".png", "")
                    .replace("_", " ")
                    .title()
                ),

                use_container_width=True

            )

        else:

            st.warning(
                f"{chart} not found."
            )







