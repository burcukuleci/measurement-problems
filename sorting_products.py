###################################################
# Sorting Products
###################################################

###################################################
# Practice: Sorting Courses
###################################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("datasets/product_sorting.csv")
print(df.shape)
df.head(10)

## Columns:

# course_name
# instructor_name
# purchase_count
# rating: rating for the course
# comment_count: total comment count for the course
# 5_point: count of 5 rating
# 4_point: count of 4 rating
# 3_point: count of 3 rating
# 2_point: count of 2 rating
# 1_point: count of 1 rating


####################
# Sorting by Rating
####################

df.sort_values("rating", ascending=False).head(20)

# >> We overlook the effect of the number of purchases and comments.

####################
# Sorting by Comment Count or Purchase Count
####################

df.sort_values("purchase_count", ascending=False).head(5)
df.sort_values("comment_count", ascending=False).head(5)

# When sorting by purchase count some courses with high comment count are falling behind in the ranking.



####################
# Sorting by Rating, Comment Count and Purchase Count
####################

# Scale to keep the impact of the number of reviews and sales on the score equal.
# Scaling counts between 1 and 5.

df["purchase_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["purchase_count"]]). \
    transform(df[["purchase_count"]])

df["comment_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["comment_count"]]). \
    transform(df[["comment_count"]])

df.describe().T

# Calculate weighted_sorting_score for each course using "comment_count_scaled", "purchase_count_scaled" and "rating"

def weighted_sorting_score(dataframe, w1=32, w2=26, w3=42):
    return (dataframe["comment_count_scaled"] * w1 / 100 +
            dataframe["purchase_count_scaled"] * w2 / 100 +
            dataframe["rating"] * w3 / 100)

# calculate weighted sorting score for each course.
df["weighted_sorting_score"] = weighted_sorting_score(df)

df.sort_values("weighted_sorting_score", ascending=False).head(20)

# list the top 20 courses that contain "Veri Bilimi" in the course name
df[df["course_name"].str.contains("Veri Bilimi")].sort_values("weighted_sorting_score", ascending=False).head(20)



####################
# Bayesian Average Rating Score
####################

# Sorting Products with 5 Star Rated
# Sorting Products According to Distribution of 5 Star Rating

# n: number of ratings in the order of scale 1, 2, 3, 4, 5
# confidence: confidence interval 95%

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


# apply the function to each row/course and create a new column for the scores: "bar_score"

df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                "2_point",
                                                                "3_point",
                                                                "4_point",
                                                                "5_point"]]), axis=1)

df.sort_values("weighted_sorting_score", ascending=False).head(5)
df.sort_values("bar_score", ascending=False).head(5)

df[df["course_name"].index.isin([5, 1])].sort_values("bar_score", ascending=False)


####################
# Hybrid Sorting: BAR Score + Other Factors
####################

# - Hybrid Sorting: BAR Score + Other Factors

def hybrid_sorting_score(dataframe, bar_w=60, wss_w=40):
    # calculate bayesian average rating
    bar_score = dataframe.apply(
        lambda x: bayesian_average_rating(x[["1_point", "2_point", "3_point", "4_point", "5_point"]]), axis=1)

    # calculate weighted sorting score
    wss_score = weighted_sorting_score(dataframe)

    # calculate hybrid weighted sorting score
    return bar_score * bar_w / 100 + wss_score * wss_w / 100


df["hybrid_sorting_score"] = hybrid_sorting_score(df)

df.sort_values("hybrid_sorting_score", ascending=False).head(20)


df.sort_values("hybrid_sorting_score", ascending=False)[["course_name", "purchase_count", "comment_count", "rating", "weighted_sorting_score",  "bar_score",  "hybrid_sorting_score"]].head(20)

