# RATING PRODUCTS

Calculating the rating of a product using various factors.

## PROJECT: Rating Course Using User-Based and Time-Based Weighted Average

This project provides a comprehensive approach to rating a course using various average methods. 

In this project, we use a dataset of course reviews to demonstrate different methods of calculating ratings.

**Methods** 

- [Average Rating](#average-rating): Calculates the simple average of all ratings.
- [Time-Based Weighted Average](#timebased-weighted-average): Gives more weight to recent ratings.
- [User-Based Weighted Average](#userbased-weighted-average): Gives more weight to ratings from users who have made more 
progress in the course.
- [Combined Weighted Rating](#combined-weighted-rating): Combines time-based and user-based weighted averages to provide a final rating.

The script includes functionalities to calculate average ratings, time-based weighted averages, user-based weighted averages, and a combined weighted rating.

> *python file*:  [rating_products.py](rating_products.py)

- dataset: course_reviews.csv     

**Columns**:

Rating: The rating provided by the customer (5-star rating)

Timestamp: The time customer rated.

Enrolled: The time customer became a member.

Progress: The customer’s progress percentage in the course.

Question Asked: The number of questions asked by customer.

Question Answered: Number of responses received by customer.

### Average Rating

- Calculate the rating of a product with arithmetic average by defining function **average_rating**.

```python
def average_rating(df):
    return df['Rating'].mean()

average_rating=average_rating(df)
```

CONS: This method may not contain the current market trends and customer satisfaction. The rating of the product can be calculated using time-based weights.     ???????????????

### Time-Based Weighted Average

- Convert 'Timestamp' column to datetime type because it was originally object datatype.

- Assign a 'current_date' variable as a analysis date.

- Calculate the difference between 'current_date' and 'Timestamp' for each rating in day format as a new column called 'days'. 

```python
df["days"] = (current_date - df["Timestamp"]).dt.days
```

Period date ranges:

period1: 0-30 days, weight=w1

period2: 30-90 days, weight=w2

period3: 90-180 days, weight=w3

period4: more than 180 days, weight=w4

- What is the average rating for the last 30 days?

```python
dff.loc[df[‘days] < 30, ‘Rating’].mean()
```
- Calculate a weighted average where more recent ratings have higher weights.

rating = w1×avg_period1 + w2×avg_period2 + w3×avg_period3 + w4×avg_period4

```python
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_rating=time_based_weighted_average(df, 30, 26, 22, 22)
```

CONS: Until now, all users' ratings have been treated equally which can lead to misunderstanding about the course. For example, each user's rating should not be considered equal because each user's percentage of progress in the course is different.


### User-Based Weighted Average

The rating of the users with different progress in the course should not be treated equally when calculating the overall rating of the course.

In this example the rating is calculated with a weighted average where ratings from users with higher progress have higher weights. Users are divided into 4 groups according to their progress in the course.

- Calculate user-based weighted average rating by considering different weights for different progress percentages.

w1: weight for users with progress less than 10%.

w2: weight for users with progress between 10% and 45%.

w3: weight for users with progress between 45% and 75%.

w4: weight for users with progress greater than 75%.


```python
def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100

user_based_rating=user_based_weighted_average(df, 20, 24, 26, 30)
```

### Combined Weighted Rating

*The method of calculating the course rating based on both the time passed since the rating and the user's progress is more reliable.*

- Calculate rating by combining the time-based (time_w) and user-based (user_w) averages.

```python
def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100

final_weighted_average=course_weighted_rating(df, time_w=40, user_w=60)
```

### Result Rating Values:

Average Rating: 4.764

Time-Based Rating: 4.765

User-Based Rating: 4.803

Combined Rating: 4.786
