# NETFLIX DATA ANALYTICS PROJECT


import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")


os.makedirs("output", exist_ok=True)
os.makedirs("charts", exist_ok=True)

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv("data/netflix_titles.csv")

print("Dataset Loaded Successfully!\n")


print(df.head())



print("\nDataset Shape")
print(df.shape)



print("\nColumns")

for col in df.columns:
    print(col)


print("\nData Types")

print(df.dtypes)



print("\nDataset Information")

print(df.info())



print("\nMissing Values")

print(df.isnull().sum())



print("\nDuplicate Rows")

print(df.duplicated().sum())


df.drop_duplicates(inplace=True)

print("\nDuplicates Removed")



df["director"] = df["director"].fillna("Unknown")

df["cast"] = df["cast"].fillna("Not Available")

df["country"] = df["country"].fillna("Unknown")

df["rating"] = df["rating"].fillna("Not Rated")

df["duration"] = df["duration"].fillna("Unknown")
["date_added"] = df["date_adColumns..."]

# Year Added
df["year_added"] = df["date_added"].dt.year

# Month Added
df["month_added"] = df["date_added"].dt.month_name()

# Day Added
df["day_added"] = df["date_added"].dt.day



df["duration_num"] = (
    df["duration"]
    .str.extract("(\d+)")
)

df["duration_num"] = pd.to_numeric(
    df["duration_num"],
    errors="coerce"
)


df["duration_type"] = (
    df["duration"]
    .str.extract("([A-Za-z]+)")
)



df["primary_genre"] = (
    df["listed_in"]
    .str.split(",")
    .str[0]
)


df["primary_country"] = (
    df["country"]
    .str.split(",")
    .str[0]
)



df["decade"] = (
    df["release_year"] // 10
) * 10



current_year = pd.Timestamp.now().year

df["content_age"] = current_year - df["release_year"]



df.columns = [
    c.lower().replace(" ", "_")
    for c in df.columns
]

print("Feature Engineering Completed.")


print("\nMissing Values After Cleaning")

print(df.isnull().sum())



clean_path = "output/netflix_cleaned.csv"

df.to_csv(clean_path, index=False)

print("\nClean Dataset Saved Successfully")

print(clean_path)


print("\nClean Dataset Preview")

print(df.head())

print("\nTotal Rows :", len(df))
print("Total Columns :", len(df.columns))

print("\nPart 1A Completed Successfully.")



print("\n" + "="*60)
print("EXPLORATORY DATA ANALYSIS")
print("="*60)



print("\nSummary Statistics")

print(df.describe(include='all'))


print("\nUnique Values")

for col in df.columns:
    print(f"{col:20} : {df[col].nunique()}")



print("\nMemory Usage")

memory = df.memory_usage(deep=True).sum()/1024/1024

print(f"{memory:.2f} MB")



print("\nMovies vs TV Shows")

print(df["type"].value_counts())



print("\nTop 20 Release Years")

print(df["release_year"].value_counts().head(20))



print("\nTop 10 Countries")

country = (
    df["primary_country"]
    .value_counts()
    .head(10)
)

print(country)



print("\nTop Genres")

genre = (
    df["primary_genre"]
    .value_counts()
    .head(10)
)

print(genre)


print("\nRatings")

ratings = (
    df["rating"]
    .value_counts()
)

print(ratings)



print("\nTop Directors")

directors = (
    df[df["director"]!="Unknown"]
    ["director"]
    .value_counts()
    .head(10)
)

print(directors)



print("\nTop Actors")

actors = (
    df[df["cast"]!="Not Available"]
    ["cast"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

print(actors)



movies = df[df["type"]=="Movie"]

print("\nAverage Movie Duration")

print(round(movies["duration_num"].mean(),2),"Minutes")


tv = df[df["type"]=="TV Show"]

print("\nAverage Seasons")

print(round(tv["duration_num"].mean(),2))



print("\nEarliest Release")

print(df["release_year"].min())

print("\nLatest Release")

print(df["release_year"].max())



print("\nContent Added Every Year")

content_added = (
    df["year_added"]
    .value_counts()
    .sort_index()
)

print(content_added)



missing = pd.DataFrame({
    "Column":df.columns,
    "Missing Values":df.isnull().sum().values,
    "Percentage":(
        df.isnull().sum()/len(df)*100
    ).round(2).values
})

print("\nMissing Value Report")

print(missing)

missing.to_csv(
    "output/missing_report.csv",
    index=False
)



dtype_report = pd.DataFrame({
    "Column":df.columns,
    "Datatype":df.dtypes.values
})

dtype_report.to_csv(
    "output/datatypes.csv",
    index=False
)



print("\nBusiness KPIs")

print("-"*40)

print("Total Titles :",len(df))

print("Movies :",len(df[df["type"]=="Movie"]))

print("TV Shows :",len(df[df["type"]=="TV Show"]))

print("Countries :",df["primary_country"].nunique())

print("Genres :",df["primary_genre"].nunique())

print("Directors :",df["director"].nunique())

print("Actors :",actors.shape[0])

print("Latest Release :",df["release_year"].max())

print("Oldest Release :",df["release_year"].min())

print("Average Movie Duration :",
round(movies["duration_num"].mean(),2))

print("Average TV Seasons :",
round(tv["duration_num"].mean(),2))

print("Most Popular Genre :",
genre.idxmax())

print("Top Country :",
country.idxmax())

print("Most Common Rating :",
ratings.idxmax())



kpi = pd.DataFrame({

"KPI":[

"Total Titles",
"Movies",
"TV Shows",
"Countries",
"Genres",
"Directors",
"Latest Release",
"Oldest Release"

],

"Value":[

len(df),
len(df[df["type"]=="Movie"]),
len(df[df["type"]=="TV Show"]),
df["primary_country"].nunique(),
df["primary_genre"].nunique(),
df["director"].nunique(),
df["release_year"].max(),
df["release_year"].min()

]

})

kpi.to_csv(
    "output/kpi_report.csv",
    index=False
)

print("\nEDA Completed Successfully.")

print("\nReports Saved Inside Output Folder")









print("\nGenerating Charts...")

plt.style.use("ggplot")



plt.figure(figsize=(7,7))

df["type"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    explode=(0.03,0.03)
)

plt.title("Movies vs TV Shows")
plt.ylabel("")
plt.tight_layout()

plt.savefig("charts/chart1_movies_vs_tvshows.png", dpi=300)

plt.close()




plt.figure(figsize=(12,6))

genre = df["primary_genre"].value_counts().head(10)

sns.barplot(
    x=genre.values,
    y=genre.index
)

plt.title("Top 10 Genres")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()

plt.savefig("charts/chart2_top_genres.png", dpi=300)

plt.close()



plt.figure(figsize=(12,6))

country = df["primary_country"].value_counts().head(10)

sns.barplot(
    x=country.values,
    y=country.index
)

plt.title("Top 10 Countries")
plt.xlabel("Titles")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("charts/chart3_top_countries.png", dpi=300)

plt.close()




plt.figure(figsize=(12,6))

sns.countplot(
    data=df,
    x="rating",
    order=df["rating"].value_counts().index
)

plt.xticks(rotation=45)

plt.title("Ratings Distribution")

plt.tight_layout()

plt.savefig("charts/chart4_ratings.png", dpi=300)

plt.close()




plt.figure(figsize=(14,6))

release=df["release_year"].value_counts().sort_index()

plt.plot(
    release.index,
    release.values,
    linewidth=2
)

plt.title("Content Release Trend")

plt.xlabel("Release Year")

plt.ylabel("Titles")

plt.tight_layout()

plt.savefig("charts/chart5_release_trend.png",dpi=300)

plt.close()




plt.figure(figsize=(12,6))

added=df["year_added"].value_counts().sort_index()

plt.plot(
    added.index,
    added.values,
    marker="o"
)

plt.title("Content Added to Netflix")

plt.xlabel("Year")

plt.ylabel("Titles")

plt.tight_layout()

plt.savefig("charts/chart6_content_added.png",dpi=300)

plt.close()


plt.figure(figsize=(12,6))

director=df[
df["director"]!="Unknown"
]["director"].value_counts().head(10)

sns.barplot(
    x=director.values,
    y=director.index
)

plt.title("Top Directors")

plt.xlabel("Titles")

plt.ylabel("Director")

plt.tight_layout()

plt.savefig("charts/chart7_directors.png",dpi=300)

plt.close()




actor=df[
df["cast"]!="Not Available"
]["cast"].str.split(", ").explode()

actor=actor.value_counts().head(10)

plt.figure(figsize=(12,6))

sns.barplot(
    x=actor.values,
    y=actor.index
)

plt.title("Top Actors")

plt.xlabel("Titles")

plt.ylabel("Actor")

plt.tight_layout()

plt.savefig("charts/chart8_actors.png",dpi=300)

plt.close()




plt.figure(figsize=(12,6))

sns.histplot(
    data=df[df["type"]=="Movie"],
    x="duration_num",
    bins=30,
    kde=True
)

plt.title("Movie Duration Distribution")

plt.xlabel("Minutes")

plt.tight_layout()

plt.savefig("charts/chart9_movie_duration.png",dpi=300)

plt.close()




plt.figure(figsize=(12,6))

sns.countplot(
    data=df[df["type"]=="TV Show"],
    x="duration_num"
)

plt.title("TV Show Seasons")

plt.xlabel("Number of Seasons")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/chart10_tvshow_seasons.png",dpi=300)

plt.close()

print("Charts 1-10 Generated Successfully.")



plt.figure(figsize=(10,6))

decade = df["decade"].value_counts().sort_index()

sns.barplot(
    x=decade.index.astype(str),
    y=decade.values
)

plt.title("Content Distribution by Decade")
plt.xlabel("Decade")
plt.ylabel("Number of Titles")
plt.tight_layout()

plt.savefig("charts/chart11_decade_distribution.png", dpi=300)

plt.close()


plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="content_age",
    bins=20,
    kde=True
)

plt.title("Content Age Distribution")
plt.xlabel("Content Age (Years)")
plt.tight_layout()

plt.savefig("charts/chart12_content_age.png", dpi=300)

plt.close()



plt.figure(figsize=(12,6))

movies = (
    df[df["type"]=="Movie"]
    ["release_year"]
    .value_counts()
    .sort_index()
)

plt.plot(
    movies.index,
    movies.values,
    linewidth=2
)

plt.title("Movies Released Per Year")
plt.xlabel("Release Year")
plt.ylabel("Movies")

plt.tight_layout()

plt.savefig("charts/chart13_movies_per_year.png", dpi=300)

plt.close()



plt.figure(figsize=(12,6))

tv = (
    df[df["type"]=="TV Show"]
    ["release_year"]
    .value_counts()
    .sort_index()
)

plt.plot(
    tv.index,
    tv.values,
    linewidth=2
)

plt.title("TV Shows Released Per Year")
plt.xlabel("Release Year")
plt.ylabel("TV Shows")

plt.tight_layout()

plt.savefig("charts/chart14_tvshows_per_year.png", dpi=300)

plt.close()



plt.figure(figsize=(12,6))

top_years = (
    df["release_year"]
    .value_counts()
    .head(15)
)

sns.barplot(
    x=top_years.index.astype(str),
    y=top_years.values
)

plt.xticks(rotation=45)

plt.title("Top 15 Release Years")

plt.tight_layout()

plt.savefig("charts/chart15_top_release_years.png", dpi=300)

plt.close()


plt.figure(figsize=(8,8))

genre = df["primary_genre"].value_counts().head(5)

plt.pie(
    genre.values,
    labels=genre.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Top 5 Genres")

plt.tight_layout()

plt.savefig("charts/chart16_genre_pie.png", dpi=300)

plt.close()



plt.figure(figsize=(8,8))

country = df["primary_country"].value_counts().head(5)

plt.pie(
    country.values,
    labels=country.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Top 5 Countries")

plt.tight_layout()

plt.savefig("charts/chart17_country_pie.png", dpi=300)

plt.close()



plt.figure(figsize=(10,6))

sns.boxplot(
    data=df[df["type"]=="Movie"],
    x="duration_num"
)

plt.title("Movie Duration Boxplot")

plt.tight_layout()

plt.savefig("charts/chart18_boxplot.png", dpi=300)

plt.close()



plt.figure(figsize=(8,6))

corr = df[
    ["release_year","duration_num","content_age"]
].corr(numeric_only=True)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("charts/chart19_heatmap.png", dpi=300)

plt.close()


plt.figure(figsize=(10,6))

missing = df.isnull().sum()

sns.barplot(
    x=missing.index,
    y=missing.values
)

plt.xticks(rotation=45)

plt.title("Missing Values After Cleaning")

plt.tight_layout()

plt.savefig("charts/chart20_missing_values.png", dpi=300)

plt.close()

print("="*50)
print("ALL 20 CHARTS GENERATED SUCCESSFULLY")
print("="*50)

print("\nCharts saved inside 'charts' folder.")



print()

print("="*60)

print("PROJECT COMPLETED SUCCESSFULLY")

print("="*60)