
############################################
# Project: IMDB Movie Scoring & Sorting
############################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("datasets/movies_metadata.csv", low_memory=False)

# select necessary columns
df = df[["title", "vote_average", "vote_count"]]
df.describe()
df.head()


########################
# Sorting According to 'Vote Average'
########################

df.sort_values("vote_average", ascending=False).head(10)


########################
# vote_average * vote_count
########################

# check the distribution of vote_count

df["vote_count"].describe([0.10, 0.25, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99]).T

# filter the movies having less than 400 vote count
df[df["vote_count"] > 400].sort_values("vote_average", ascending=False).head(20)

# scale 'vote_count' between 1 and 10.
df["vote_count_score"] = MinMaxScaler(feature_range=(1, 10)).fit(df[["vote_count"]]).transform(df[["vote_count"]])

df["average_count_score"] = df["vote_average"] * df["vote_count_score"]

df.sort_values("average_count_score", ascending=False).head(20)


########################
# IMDB Weighted Rating
########################


# weighted_rating = (v/(v+M) * r) + (M/(v+M) * C)

# r = vote average
# v = vote count
# M = minimum votes required to be listed in the Top 250
# C = the mean vote across the whole report (currently 7.0)

M = 2500
C = df['vote_average'].mean()

def weighted_rating(r, v, M, C):
    return (v / (v + M) * r) + (M / (v + M) * C)

df.sort_values("average_count_score", ascending=False).head(10)

df["weighted_rating"] = weighted_rating(df["vote_average"], df["vote_count"], M, C)

df.sort_values("weighted_rating", ascending=False).head(10)


# TOP 5 Movies according to "weighted_rating" using equation

# 12481                                    The Dark Knight
# 314                             The Shawshank Redemption
# 2843                                          Fight Club
# 15480                                          Inception
# 292                                         Pulp Fiction



####################
# Bayesian Average Rating Score
####################

def bayesian_average_rating(n, confidence=0.95):
    # return 0 in the case of no rating
    if sum(n) == 0:
        return 0

    K = len(n)   # number of rating category
    # positive critical z-value for corresponding area
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)   # total count of ratings
    first_part = 0.0
    second_part = 0.0

    # calculate first_part and second_part for each rating category then use them to calculate score
    for k, n_k in enumerate(n):
        first_part += (k + 1) * (n[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n[k] + 1) / (N + K)
    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score


df = pd.read_csv("datasets/imdb_ratings.csv")

# csv file contains 1-10 score rating counts for movies

# Columns: 'id', 'movieName', 'rating', 'ten', 'nine', 'eight', 'seven', 'six', 'five', 'four', 'three', 'two', 'one'
# drop 'Unnamed: 0' column (it is index column, we already have indices)
df = df.iloc[0:, 1:]

# calculate BAR score for each movie using Bayesian Average method

df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["one", "two", "three", "four", "five",
                                                                "six", "seven", "eight", "nine", "ten"]]), axis=1)

# sort movie ranking according to bar score

df.sort_values("bar_score", ascending=False)[["movieName", "rating", "bar_score"]].head(10)

# movieName  rating  bar_score
# 0  1.       The Shawshank Redemption (1994) 9.20000    9.14539
# 1             2.       The Godfather (1972) 9.10000    8.94002
# 3           4.       The Dark Knight (2008) 9.00000    8.89596
# 2    3.       The Godfather: Part II (1974) 9.00000    8.81250
# 4              5.       12 Angry Men (1957) 8.90000    8.76793


