############################################
# SORTING REVIEWS
############################################

import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


###################################################
# Up-Down Diff Score = (up ratings) − (down ratings)
###################################################

# Review 1: 600 up 400 down total 1000
# Review 2: 5500 up 4500 down total 10000

def score_up_down_diff(up, down):
    return up - down

# Review 1 Score: 200
score_up_down_diff(600, 400)

# Review 2 Score: 1000
score_up_down_diff(5500, 4500)


###################################################
# Score = Average rating = (up ratings) / (all ratings)
###################################################

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)


# Review 1: 2 up 0 down total 2
score_average_rating(2, 0)   # 1.0

# Review 2: 100 up 1 down total 101
score_average_rating(100, 1)    # 0.99

score_average_rating(2, 1)    # 0.66

score_average_rating(600, 400)   # 0.6

score_average_rating(5500, 4500)   # 0.5




###################################################
# Wilson Lower Bound Score
###################################################

# up-voting: 600
# down-voting: 400
# up voting rate: 0.6
# confidence interval: 0.5 0.7

# Statistically, when 95 out of 100 users interact with this review,
# we say that although we have a 5% margin of error, the up voting rate of this review will be between 0.5 and 0.7.

# Calculate Wilson Lower Bound Score for a review using up-vote and down-vote of a review.


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


wilson_lower_bound(100, 1)       # 0.94
wilson_lower_bound(600, 400)     # 0.56
wilson_lower_bound(5500, 4500)   # 0.54
wilson_lower_bound(2, 0)         # 0.34


###################################################
# Case Study
###################################################

# upvote and downvote counts for 22 reviews of a product are converted to a dataframe.

up = [15, 70, 14, 4, 2, 5, 8, 37, 21, 52, 28, 147, 61, 30, 23, 40, 37, 61, 54, 18, 12, 68]
down = [0, 2, 2, 2, 15, 2, 6, 5, 23, 8, 12, 2, 1, 1, 5, 1, 2, 6, 2, 0, 2, 2]
comments = pd.DataFrame({"up": up, "down": down})


# score_pos_neg_diff
comments["score_pos_neg_diff"] = comments.apply(lambda x: score_up_down_diff(x["up"], x["down"]), axis=1)

# score_average_rating
comments["score_average_rating"] = comments.apply(lambda x: score_average_rating(x["up"], x["down"]), axis=1)

# wilson_lower_bound
comments["wilson_lower_bound"] = comments.apply(lambda x: wilson_lower_bound(x["up"], x["down"]), axis=1)

comments.head()

# # TOP 6 reviews
comments.sort_values("wilson_lower_bound", ascending=False).head(6)








