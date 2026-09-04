import pandas as pd
import urllib.request
import gzip
import os
from datetime import datetime
ratings_url = "https://datasets.imdbws.com/title.ratings.tsv.gz"
basics_url = "https://datasets.imdbws.com/title.basics.tsv.gz"
print("Downloading IMDb ratings...")
with urllib.request.urlopen(ratings_url) as response:
    with gzip.GzipFile(fileobj=response) as f:
        ratings = pd.read_csv(
            f,
            sep="\t",
            na_values="\\N"
        )
print("Downloading IMDb movie data...")
with urllib.request.urlopen(basics_url) as response:
    with gzip.GzipFile(fileobj=response) as f:
        basics = pd.read_csv(
            f,
            sep="\t",
            na_values="\\N",
            low_memory=False
        )
movies = basics[
    basics["titleType"] == "movie"
].copy()
movies = movies[
    [
        "tconst",
        "primaryTitle",
        "startYear"
    ]
]
ratings = ratings[
    [
        "tconst",
        "averageRating",
        "numVotes"
    ]
]
df = movies.merge(
    ratings,
    on="tconst",
    how="inner"
)
df = df.dropna(
    subset=[
        "primaryTitle",
        "startYear",
        "averageRating",
        "numVotes"
    ]
)
df = df.sort_values(
    by=[
        "averageRating",
        "numVotes"
    ],
    ascending=[
        False,
        False
    ]
)
df = df.head(200).copy()
timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)
final_df = pd.DataFrame({
    "timestamp": timestamp,
    "rank": range(1, len(df) + 1),
    "movie_name": df["primaryTitle"].values,
    "year": df["startYear"].astype(int).values,
    "rating": df["averageRating"].values,
    "votes": df["numVotes"].astype(int).values
})
folder = "IMDb_Movie_Data"
os.makedirs(
    folder,
    exist_ok=True
)
csv_file = os.path.join(
    folder,
    "imdb_top_200_movies.csv"
)
excel_file = os.path.join(
    folder,
    "imdb_top_200_movies.xlsx"
)
final_df.to_csv(
    csv_file,
    index=False,
    encoding="utf-8-sig"
)
final_df.to_excel(
    excel_file,
    index=False
)
print("\n====================================")
print("IMDb TOP 200 MOVIES")
print("====================================")
print(final_df.to_string(index=False))
print("\n====================================")
print("FILES SAVED")
print("====================================")
print(
    "CSV:",
    os.path.abspath(csv_file)
)
print(
    "Excel:",
    os.path.abspath(excel_file)
)

print("\nTotal movies:", len(final_df))