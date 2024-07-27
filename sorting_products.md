# SORTING PRODUCT

Sorting products according to the score calculated using the course rating and other factors.

**Methods:**

1. **Sorting by Rating, Comment Count and Purchase Count**: Weighted sorting score
2. **Bayesian Average Rating Score (BAR Score)**: Bayesian average has a better balance of rating and quantity of rating. It ensures that products with lower numbers of ratings have less weight in the ranking.
3. **Hybrid Sorting**: Calculate weighted score using both "bar score" and "weighted sorting score".

> *python file*:  [sorting_products.py](sorting_products.py)

- dataset: product_sorting.csv    

**Columns:**

course_name: name of the course

purchase_count: number of the total purchases

rating: rating for the course

comment_count: number of total comments for the course

5_point, 4_point, 3_point, 2_point, 1_point: counts of rating values


## Sorting by Rating, Comment Count and Purchase Count

- Scale comment and purchase counts with *MinMaxScaler* to range (1,5) in order to keep the impact of rating, comment count and purchase count equal.

- Calculate weighted sorting score for each course using "comment_count_scaled", "purchase_count_scaled" and "rating" columns.

```python
def weighted_sorting_score(dataframe, w1=32, w2=26, w3=42):
    return (dataframe["comment_count_scaled"] * w1 / 100 +
            dataframe["purchase_count_scaled"] * w2 / 100 +
            dataframe["rating"] * w3 / 100)

# calculate weighted sorting score for each course.
df["weighted_sorting_score"] = weighted_sorting_score(df)
```

## Bayesian Average Rating Score (BAR Score)

Sorting Products According to Distribution of 5 Star Rating.

- Calculate Bayesian Average Rating (BAR) score with ***bayesian_average_rating*** function.

n: number of ratings in the order of scale 1, 2, 3, 4, 5

confidence: confidence interval 95%

```python
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
df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["1_point","2_point", "3_point", "4_point", "5_point"]]), axis=1)
```

## Hybrid Sorting

Hybrid Sorting: BAR Score (Bayesian) + Other Factor (Weighted Score)

- Create new column 'hybrid_sorting_score' with *hybrid_sorting_score* function.

```python
def hybrid_sorting_score(dataframe, bar_w=60, wss_w=40):
    # calculate bayesian average rating
    bar_score = dataframe.apply(lambda x: bayesian_average_rating(x[["1_point", "2_point", "3_point", "4_point", "5_point"]]), axis=1)
    
    # calculate weighted sorting score
    wss_score = weighted_sorting_score(dataframe)
     
    # calculate hybrid weighted sorting score
    return bar_score*bar_w/100 + wss_score*wss_w/100

df["hybrid_sorting_score"] = hybrid_sorting_score(df)
```

- first 5 courses with highest hybrid_sorting_score >>

```
                                          course_name  purchase_count  comment_count  rating  weighted_sorting_score  bar_score  hybrid_sorting_score
1   Python: Yapay Zeka ve Veri Bilimi için Python ...           48291           4488 4.60000                 4.79510    4.51604               4.62766
0   (50+ Saat) Python A-Z™: Veri Bilimi ve Machine...           17380           4621 4.80000                 4.24988    4.66586               4.49947
20                                           Course_9           12946           3371 4.50000                 3.68156    4.48063               4.16100
10        İleri Düzey Excel|Dashboard|Excel İp Uçları            9554           2266 4.80000                 3.42792    4.64168               4.15618
14                       Uçtan Uca SQL Server Eğitimi           12893           2425 4.70000                 3.50198    4.56816               4.14169
```