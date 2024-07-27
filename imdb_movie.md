# PROJECT: IMDB Movie Scoring Sorting

Sort movies by rating using hybrid scoring method.

Then, compare the order of the top movies with IMDB rating values and movie order.

**Methods:**

1. **Vote Average**: Sort movies by 'vote_average'.
2. **Average Count Score**: vote_average * vote_count
3. **IMDB Weighted Rating**: Use the weighted rating equation.
4. **Bayesian Average Rating (BAR) Score**: : Bayesian average has a better balance of rating and quantity of rating. It ensures that products with lower numbers of ratings have less weight in the ranking.

> *python file*:  [imdb_movie.py](imdb_movie.py)

- dataset: movies_metadata.csv

**Columns:**

title: movie titles

vote_average: average of the ratings for a movie

vote_count: number of vote/rating for a movie


## Vote Average

Sort movies by 'vote_average'.

CON: This method favors the movies having low vote count with high votes.

## Average Count Score

Calculate a score bu considering both vote_average and vote_count.

- Filter the movies with vote count lower than 400.

- Scale vote_count using *MinMaxScaler* to range 0f 1 to 10 in order to make the impact of vote_average and vote_count equal. : "vote_count_score"

- Calculate "average_count_score" by multiplying "vote_average" and "vote_count_score".

```python
df["average_count_score"] = df["vote_average"] * df["vote_count_score"]
```

## IMDB Weighted Rating

Use the equation to calculate weighted rating of movies.

**weighted_rating = (v/(v+M) * r) + (M/(v+M) * C)**

- r = vote average
- v = vote count
- M = minimum votes required to be listed in the Top 250
- C = the mean vote across the whole report (currently 7.0)

- Calculate weightes rating using ***weighted_rating*** function. 

```python
M = 2500
C = df['vote_average'].mean()

def weighted_rating(r, v, M, C):
    return (v / (v + M) * r) + (M / (v + M) * C)

df["weighted_rating"] = weighted_rating(df["vote_average"], df["vote_count"], M, C)
```

## Bayesian Average Rating (BAR) Score

Calculate BAR scores and compare with IMDB rating values.

Compare the order of the top movies.

- dataset: imdb_rating.csv

***Columns**:

id: movie ID

movieName: name of the movie

rating: IMDB rating value (1-10 scale)

ten, nine, eight, seven, six, five, four, three, two, one: number of ratings for each rating value

- Calculate BAR score.

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

df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["one", "two", "three", "four", "five",
                                                                "six", "seven", "eight", "nine", "ten"]]), axis=1)
```

- Sort movie ranking according to bar score.

```python
# TOP 5 movies
df.sort_values("bar_score", ascending=False)[["movieName", "rating", "bar_score"]].head(5)
```

- **TOP 5 movies by BAR SCORE**

```
                                  movieName  rating  bar_score

0  1.       The Shawshank Redemption (1994) 9.20000    9.14539

1             2.       The Godfather (1972) 9.10000    8.94002

3           4.       The Dark Knight (2008) 9.00000    8.89596

2    3.       The Godfather: Part II (1974) 9.00000    8.81250

4              5.       12 Angry Men (1957) 8.90000    8.76793
```