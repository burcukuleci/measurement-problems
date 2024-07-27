
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


############################
# Confidence Intervals & Correlation
############################

df = sns.load_dataset("tips")
df.describe()
df.head()

# tips dataset columns:
# total_bill: total bill of the meal (with the tip)
# tip: amount of the tip
# sex: sex of the customer who paid the bill (0=male, 1=female)
# smoker: is there a smoker in the group? (0=No, 1=Yes)
# day: day of the week (3=Thur, 4=Fri, 5=Sat, 6=Sun)
# time: time of the day (0=Day, 1=Night)
# size: number of the person in the group

# Calculate confidence interval for numerical columns in the 'tips' dataset
sms.DescrStatsW(df["total_bill"]).tconfint_mean()
sms.DescrStatsW(df["tip"]).tconfint_mean()


# calculate money of the meal by substracting tip from total_bill
df["total_bill"] = df["total_bill"] - df["tip"]

df.plot.scatter("tip", "total_bill")
plt.show()

# Calculate correlation between tip and total_bill.
df["tip"].corr(df["total_bill"])



######################################################
# AB Testing (Independent Two Sample T-test)
######################################################

# 1. Establish Hypotheses
# 2. Assumption Checking
#   - 2.1. Normality Assumption
#   - 2.2. Assumption of Homogeneity of Variance
# 3. Application of Hypotheses
#   - 3.1. If the assumptions are met, independent two-sample t test (parametric test)
#   - 3.2. If the assumptions are not met, mannwhitneyu test (non-parametric test)
# 4. Interpret the results according to the p-value
# Note:
# - If normality is not ensured, apply step 2 directly. If variance homogeneity is not achieved, enter argument to step 1.
# - It may be useful to perform outlier review and correction before normality review.



############################
#### CASE 1: Is there a statistical difference between the total bill averages of smokers and non-smokers?
############################


df = sns.load_dataset("tips")
df.head()

# mean of the total_bill for smoker and non-smoker groups
df.groupby("smoker").agg({"total_bill": "mean"})


### 1. Establish Hypotheses

# H0: M1 = M2
# H1: M1 != M2


### 2. Assumption Checking

## Normality Assumption

# H0: Normality assumption is met.
# H1: Normality assumption is not met.

# test normality for two groups seperately.

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "Yes", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "No", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p values are smaller than 0.05 >> HO is rejected, normality assumption is not met.


## Assumption of Homogeneity of Variance

# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.

test_stat, pvalue = levene(df.loc[df["smoker"] == "Yes", "total_bill"],
                           df.loc[df["smoker"] == "No", "total_bill"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p value is smaller than 0.05 >> HO is rejected, assumption is not met.

# Both of the assumptions are not met, non-parametric test will be applied.


### 3 ve 4. Application of Hypotheses & Interpret the results according to the p-value.

# 3.1 If the assumptions are met, independent two-sample t test (parametric test)

test_stat, pvalue = ttest_ind(df.loc[df["smoker"] == "Yes", "total_bill"],
                              df.loc[df["smoker"] == "No", "total_bill"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# 3.2 If the assumptions are not met, mannwhitneyu test (non-parametric test)

test_stat, pvalue = mannwhitneyu(df.loc[df["smoker"] == "Yes", "total_bill"],
                                 df.loc[df["smoker"] == "No", "total_bill"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Result: Two assumption were not met. Non-parametric test is done.
# p-value is 0.34. (p >= 0.05) H0 is not rejected. There is no significant difference between two groups.



############################
### CASE 2: Is There a Statistically Significant Difference Between the Average Ages of Titanic Female and Male Passengers?
############################

df = sns.load_dataset("titanic")
df.head()

df.groupby("sex").agg({"age": "mean"})


### 1. Establish Hypotheses:
# H0: M1  = M2 (There is no statistically significant difference between the average age of males and females.)
# H1: M1! = M2 (There is statistically significant difference.)


### 2. Assumption Checking

## Normality Assumption
# H0: Normality Assumption is met.
# H1: Normality Assumption is not met.


test_stat, pvalue = shapiro(df.loc[df["sex"] == "female", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["sex"] == "male", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p values are smaller than 0.05 >> HO is rejected, assumption is not met.


## Assumption of Homogeneity of Variance
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.

test_stat, pvalue = levene(df.loc[df["sex"] == "female", "age"].dropna(),
                           df.loc[df["sex"] == "male", "age"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# # p value is greater than 0.05 >> HO is not rejected, assumption is met.

# >>> Normality assumption is not so non-parametric test will be applied.

test_stat, pvalue = mannwhitneyu(df.loc[df["sex"] == "female", "age"].dropna(),
                                 df.loc[df["sex"] == "male", "age"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Result: Non-parametric test is applied. p-value is 0.02 which smaller than 0.05 so H0 is rejected.
#         There is statistically significant difference between two groups.





############################
### CASE 3: Is there a statistically significant difference between the average ages of people with and without diabetes?
############################

df = pd.read_csv("datasets/diabetes.csv")
df.head()

df.groupby("Outcome").agg({"Age": "mean"})

### 1. Establish Hypotheses
# H0: M1 = M2 (no statistically significant difference)
# H1: M1 != M2 (statistically significant difference)


### 2. Assumption Checking

## Normality Assumption (H0: Normal distribution assumption is met.)

test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 1, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# >>> p-values are 0, H0 is rejected, normality assumption is not met, non-parametric test will be applied.

### Non-parametric test

# Hipotez (H0: M1 = M2)

test_stat, pvalue = mannwhitneyu(df.loc[df["Outcome"] == 1, "Age"].dropna(),
                                 df.loc[df["Outcome"] == 0, "Age"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Result: Non-parametric test is applied. p-value is 0 which smaller than 0.05 so H0 is rejected.
#         There is statistically significant difference two groups.




###################################################
# BUSINESS PROBLEM: Are the ratings of those who watched the majority of the course different from those who did not?
###################################################

# H0: M1 = M2  (There is no significant difference between the averages of the two groups.)
# H1: M1 != M2 (There is significant difference between the averages of the two groups.)

df = pd.read_csv("datasets/course_reviews.csv")
df.head()

df[(df["Progress"] > 75)]["Rating"].mean()

df[(df["Progress"] < 25)]["Rating"].mean()

## Normality Assumption

test_stat, pvalue = shapiro(df[(df["Progress"] > 75)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


test_stat, pvalue = shapiro(df[(df["Progress"] < 25)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-values are smaller than 0.05, H0 is rejected, normality assumption is not met. Non-parametric test will be applied.

### Non-parametric test

test_stat, pvalue = mannwhitneyu(df[(df["Progress"] > 75)]["Rating"],
                                 df[(df["Progress"] < 25)]["Rating"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value is zero, main H0 is rejected, there is statistically significant difference between distribution of two groups' ratings.




######################################################
# AB Testing (Two Sample Proportion Test)
######################################################

# H0: p1 = p2
# There is no statistically significant difference between the conversion rate of the new design and the conversion rate of the old design.
# H1: p1 != p2
# there is ...

success_count = np.array([300, 250])
sample_size = np.array([1000, 1100])

proportions_ztest(count=success_count, nobs=sample_size)

# success rate of two groups: 0.3 & 0.23
success_count / sample_size



############################
# CASE 4: Is There a Statistically Significant Difference Between the Survival Rates of Men and Women?
############################

# H0: p1 = p2
# (There is no statistically significant difference.)

# H1: p1 != p2
# (There is statistically significant difference.)

df = sns.load_dataset("titanic")
df.head()

df.loc[df["sex"] == "female", "survived"].mean()

df.loc[df["sex"] == "male", "survived"].mean()

female_succ_count = df.loc[df["sex"] == "female", "survived"].sum()
male_succ_count = df.loc[df["sex"] == "male", "survived"].sum()

test_stat, pvalue = proportions_ztest(count=[female_succ_count, male_succ_count],
                                      nobs=[df.loc[df["sex"] == "female", "survived"].shape[0],
                                            df.loc[df["sex"] == "male", "survived"].shape[0]])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value is 0, H0 is rejected. There is statistically significant difference between female and male passengers' survival rates.




######################################################
# ANOVA (Analysis of Variance)
######################################################

# It is used to compare the averages of more than two groups.

# CASE 5: Is there statistically significant difference between total bill averages of the weekdays? (Thur, Fri, Sat, Sun)

df = sns.load_dataset("tips")
df.head()

df.groupby("day")["total_bill"].mean()


### 1. Establish Hypotheses

# HO: m1 = m2 = m3 = m4
# There is no statistically significant difference between means of the groups.
# H1: There is statistically significant difference between means of the groups.

### 2. Assumption Checking

# Assumptions are met >>  one way anova (parametric anova test)
# Assumptions are not met >> kruskal (non-parametric anova test)

# -- Normality Assumption
# H0: Normality Assumption is met.

# check normality assumption for each group - print p-value for each group

for group in list(df["day"].unique()):
    pvalue = shapiro(df.loc[df["day"] == group, "total_bill"])[1]
    print(group, 'p-value: %.4f' % pvalue)

# --- all p-values of groups are smaller than 0.05 so H0 is rejected, normality assumption is not met.


# -- Assumption of Homogeneity of Variance
# H0: Assumption of Homogeneity of Variance is met.

test_stat, pvalue = levene(df.loc[df["day"] == "Sun", "total_bill"],
                           df.loc[df["day"] == "Sat", "total_bill"],
                           df.loc[df["day"] == "Thur", "total_bill"],
                           df.loc[df["day"] == "Fri", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# --- p-value is greater than 0.05 so H0 is not rejected, assumption is met.


### 3. Application of Hypotheses

# Only one assumption is met >> apply kruskal

df.groupby("day").agg({"total_bill": ["mean", "median"]})

# HO: There is no statistically significant difference between means of the groups.

# parametric anova test:

f_oneway(df.loc[df["day"] == "Thur", "total_bill"],
         df.loc[df["day"] == "Fri", "total_bill"],
         df.loc[df["day"] == "Sat", "total_bill"],
         df.loc[df["day"] == "Sun", "total_bill"])

# non-parametric anova test:

kruskal(df.loc[df["day"] == "Thur", "total_bill"],
        df.loc[df["day"] == "Fri", "total_bill"],
        df.loc[df["day"] == "Sat", "total_bill"],
        df.loc[df["day"] == "Sun", "total_bill"])

# Result: p-value of kruskal test is smaller than 0.05 so H0 is rejected, there is statistically significant difference between groups.

# find which specific groups' means (compared with each other) are different.

from statsmodels.stats.multicomp import MultiComparison
comparison = MultiComparison(df['total_bill'], df['day'])
tukey = comparison.tukeyhsd(0.05)
print(tukey.summary())