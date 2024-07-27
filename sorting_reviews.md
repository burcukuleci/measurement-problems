# SORTING REVIEWS

In what order should product reviews be displayed?

**Methods:**

1. **Up-Down Difference Score**: Substract down rating number form up rating number.
2. **Average Rating Score**: Calculate up rating percentage for a review.
3. **Wilson Lower Bound (WLB) Score**: Balance the ratio of up ratings with the uncertainty that comes from having a small number of observations.
4. **Case Study**: Apply the methods for reviews and sort the reviews by WLB score.

> *python file*:  [sorting_reviews.py](sorting_reviews.py)

- dataset: up down vote counts for reviews.

## Up-Down Difference Score

Calculate the score to sort the reviews by taking the difference between up and down ratings for a review.

**up rating**: useful review

**down rating**: not useful review

- Calulate up-down difference for given up and down count.

```python
def score_up_down_diff(up, down):
    return up - down
```

CON: This method might disregard the higher down ratings counts when the up rating count is high.

## Average Rating Score

Calculate the score to sort the reviews by finding the up-rating percentage of a review.

- ***(up ratings) / (all ratings)***

```python
def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)
```

CON: The reviews with non or very low number of down ratings might be favored by this method in the case of a low number of total reviews.

## Wilson Lower Bound (WLB) Score

We need to balance the ratio of up/positive ratings with the uncertainty that comes from having a small number of observations.

We can avoid the issue where a review with a small number of upvotes could appear highly rated just because it has a high upvote percentage. 

For a product: 5-star scale rating are divided into binary group >

               1, 2, 3: down/negative rating    &    4, 5: up/positive rating

For a review: Upvote and downvote counts for a review are considered.

> **Question:** What percentage of the user community would upvote the review with 95% confidence level?

**Example:**

    up-voting: 600

    down-voting: 400

    up voting rate: 0.6

    confidence interval: 0.5 0.7

Statistically, when 95 out of 100 users interact with this review, we say that although we have a 5% margin of error, the up-voting rate of this review will be between 0.5 and 0.7. The confidence interval (0.5 to 0.7) gives us a range within which the true upvote rate is likely to lie 95% of the time.

- Calculate Wilson Lower Bound Score for a review using up-vote and down-vote of a review.

```python
def wilson_lower_bound(up, down, confidence=0.95):
    """
    Calculate Wilson Lower Bound Score

     - The lower limit of the confidence interval to be calculated for the Bernoulli parameter p is considered as the WLB score.
     - The score to be calculated is used for product ranking.
     - Note:
     If the scores are between 1-5, 1-3 is marked as negative and 4-5 is marked as positive and can be adapted to Bernoulli.
     This brings with it some problems. For this reason, it is necessary to make a bayesian average rating.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    # total up and down rating counts for a review
    n = up + down
    if n == 0:
        return 0
    # positive z-value for confidence interval
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n   # percentage of up ratings
    # WLB score
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

```
***Most accurate and reliable score to sort reviews is WLB score.***

CON: The reviews with no upvote or downvote and the products with no reviews will have a score of zero which makes them last in the ranking.

## Case Study: 

Apply the methods for reviews and sort the reviews by WLB score.

- Create a dataframe "comments" using up and down vote counts for 22 reviews.

```python
up = [15, 70, 14, 4, 2, 5, 8, 37, 21, 52, 28, 147, 61, 30, 23, 40, 37, 61, 54, 18, 12, 68]
down = [0, 2, 2, 2, 15, 2, 6, 5, 23, 8, 12, 2, 1, 1, 5, 1, 2, 6, 2, 0, 2, 2]

comments = pd.DataFrame({"up": up, "down": down})
```
- Calculate "score_pos_neg_diff", "score_average_rating" and "wilson_lower_bound" scores by applying the above method's functions. Then sort the reviews by WLB score.

```python
# TOP 6 reviews
comments.sort_values("wilson_lower_bound", ascending=False).head(6)
```

```
     up  down  score_pos_neg_diff  score_average_rating  wilson_lower_bound
11  147     2                 145               0.98658             0.95238
12   61     1                  60               0.98387             0.91413
1    70     2                  68               0.97222             0.90426
21   68     2                  66               0.97143             0.90168
18   54     2                  52               0.96429             0.87881
15   40     1                  39               0.97561             0.87405
```
