###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# Project: Rating Course using User-Based and Time-Based Weighted Average
############################################

import pandas as pd
import math
import seaborn as sns
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Columns : Rating, Timestamp, Enrolled, Progress, Questions Asked, Questions Answered
# (50+ Saat) Python A-Z™: Veri Bilimi ve Machine Learning
# Rating: 4.8 (4.764925)
# Total Amount of Rating: 4611
# Percentages of the Ratings (5, 4, 3, 2, 1): 75, 20, 4, 1, <1

df = pd.read_csv("datasets/course_reviews.csv")
df.head()
df.shape    # (4323, 6)

# distribution of rating
df["Rating"].value_counts()
sns.histplot(df, x="Rating")

df["Questions Asked"].value_counts()

# calculate average rating for each unique number of question asked
df.groupby("Questions Asked").agg({"Questions Asked": "count",
                                   "Rating": "mean"})


####################
# Average Rating
####################

def average_rating(df):
    return df['Rating'].mean()

average_rating=average_rating(df)



####################
# Time-Based Weighted Average
####################

# check the Dtype of the columns
df.info()

# convert 'object' Timestamp to 'datetime'
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# define current time for analysis
current_date = pd.to_datetime('2021-02-10 0:0:0')

# day difference between current date and review date
df["days"] = (current_date - df["Timestamp"]).dt.days


#### Calculate averages for different periods >>

# first 30 days : 4.78
df.loc[df["days"] <= 30, "Rating"].mean()

# between 30 and 90 days : 4.77
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean()

# between 90 and 180 days : 4.75
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean()

# reviews that are older than 180 days : 4.77
df.loc[(df["days"] > 180), "Rating"].mean()


# Calculating the rate the courses by assigning weights(w1, w2, w3 and w4) for rating average of periods

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(df)

time_based_rating=time_based_weighted_average(df, 30, 26, 22, 22)

# 4.7655


####################
# User-Based Weighted Average
####################

# user quality score will be determined by considering user's progress(percentage of completing the course)

# The rating of the users that have greater progress will be weighted more.
df.groupby("Progress").agg({"Rating": "mean"})

# Calculating the rate the courses by assigning weights(w1, w2, w3 and w4) for each progress groups

def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100

user_based_rating=user_based_weighted_average(df, 20, 24, 26, 30)
# 4.8032


####################
# Weighted Rating
####################

def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100

course_weighted_rating(df)

final_weighted_average=course_weighted_rating(df, time_w=40, user_w=60)
# 4.7861

print(f'Average Rating: {average_rating}')
print(f'Time-Based Rating: {time_based_rating}')
print(f'User-Based Rating: {user_based_rating}')
print(f'Combined Rating: {final_weighted_average}')


# Average Rating: 4.764284061993986
# Time-Based Rating: 4.765491074653962
# User-Based Rating: 4.803286469062915
# Combined Rating: 4.786164895710403






