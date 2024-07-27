# AB TESTING 

In this script different statistical test methods are applied for different datasets.

- datasets: seeborn's 'tips', 'diabetes' & 'titanic' and course_reviews.csv

1. [Confidence Interval and Correlation](#confidence-interval-and-correlation)
2. [AB Testing (Independent Two Sample T-test)](#ab-testing-independent-two-sample-t-test)
3. [AB Testing (Two Sample Proportion Test)](#ab-testing-two-sample-proportion-test)
4. [ANOVA (Analysis of Variance)](#anova-analysis-of-variance)

---
## Confidence Interval and Correlation

Confidence interval gives an estimated range of values for the parameter with a level specified confidence level.

Correlation coefficient shows the linear relationship between two variables. The value lies between -1 and 1.

- Find the two sided confidence interval for columns.

```python
sms.DescrStatsW(df["tip"]).tconfint_mean()
```
- Calculate correlation between tip and total_bill.

```python
df["tip"].corr(df["total_bill"])
```

---
## AB Testing (Independent Two Sample T-test)

The t-test is used to determine whether there is a significant difference between the means of two independent groups.

**test statistics (test_stat)**: It measures the magnitude of the difference between groups.

**p-value (pvalue)**: It indicates the probability that this difference will occur randomly.

- **p < 0.05**: *There is a statistically significant difference. Reject HO.* This means that the difference between the means of the two groups is significant at the 95% confidence level. In other words, there is less than a 5% chance that this difference will occur randomly.
- **p ≥ 0.05**: *There is no statistically significant difference.* This means that the difference between the means of the two groups is not significant at the 95% confidence level.
  
**Assumptions:**

   Normal Distribution: The data of both groups must have a normal distribution.
     
   Homogeneity of Variances: It is assumed that the variances of the two groups should be equal.

**Test Steps:**


1. Establish Hypotheses

   H0: M1 = M2 -> There is no statistically significant difference between the means of the groups.

   H1: M1 != M2 -> There is a statistically significant difference between the means of the groups.
   
   p-value < 0.05 : reject H0.
   
   p-value >= 0.05 : do not reject H0.

2. Assumption Checking
   
   2.1. Normality Assumption
     
   H0: Normality assumption is met. (p-value >= 0.05)

   - Test the normality for each group with ***shapiro*** function.
   ```python
   # x1: column2 values for class1 of column1
   # x1: column2 values for class2 of column1
   
   test_stat, pvalue = shapiro(x1)
   test_stat, pvalue = shapiro(x2)
   ```
   
   2.2. Assumption of Homogeneity of Variance

   H0: Variances are homogeneous. (p-value >= 0.05)

   - Test assumption of homogeneity of variance for both two groups with ***levene*** function.

   ```python
   test_stat, pvalue = levene(x1, x2)
   ```
   
3. Application of Hypotheses
   
   3.1. If the assumptions are met, apply independent two-sample t test (parametric test)

   ```python
   test_stat, pvalue = ttest_ind(x1, x2, equal_var=True)
   ```
   
   3.2. If the assumptions are not met, apply mannwhitneyu test (non-parametric test)

   ```python
   test_stat, pvalue = mannwhitneyu(x1, x2)
   ```

4. Interpret the results according to the p-value of "ttest_ind" or "mannwhitney".
   
Note:
- If normality is not ensured, apply step 2 directly. If variance homogeneity is not achieved, enter argument to step 1.
- It may be useful to perform outlier review and correction before normality review.

Apply these independent two sample t-test steps for different cases. >>> 

> CASE 1: Is there a statistical difference between the total bill averages of smokers and non-smokers?

> CASE 2: Is there a statistically significant difference between the average ages of titanic female and male passengers?

> CASE 3: Is there a statistically significant difference between the average ages of people with and without diabetes?

> BUSINESS PROBLEM: Are the ratings of those who watched the majority of the course different from those who did not?

---
## AB Testing (Two Sample Proportion Test)

AB testing (Two Sample Proportion Test) is a statistical test used to determine whether there is a significant difference between the proportions of two independent groups.

This test is used to compare the success rates of the two groups for a particular event or characteristic.

The ***proportions_ztest*** function is used to compare the proportions of two independent samples.

```python
test_stat, pvalue = proportions_ztest(count, nobs)
# count: the number of successes for each independent sample. (e.g., [count_A, count_B])
# nobs: The number of observations (sample size). (e.g., [nobs_A, nobs_B]).
```
> CASE 4: Is there a statistically significant difference between the survival rates of men and women?

```python
female_succ_count = df.loc[df["sex"] == "female", "survived"].sum()
male_succ_count = df.loc[df["sex"] == "male", "survived"].sum()

test_stat, pvalue = proportions_ztest(count=[female_succ_count, male_succ_count],
                                      nobs=[df.loc[df["sex"] == "female", "survived"].shape[0],
                                            df.loc[df["sex"] == "male", "survived"].shape[0]])
```

---
## ANOVA (Analysis of Variance)

It is used to compare the averages of more than two groups

**Test Steps:**


1. Establish Hypotheses

   H0: M1 = M2 = M3 -> There is no statistically significant difference between the means of the groups.

   H1: M1 != M2 -> There is a statistically significant difference between the means of the groups.
   
   p-value < 0.05 : reject H0.
   
   p-value >= 0.05 : do not reject H0.

3. Assumption Checking
   
   2.1. Normality Assumption
     
   H0: Normality assumption is met. (p-value >= 0.05)

   - Test the normality for each group with ***shapiro*** function.
   ```python
   # x1: column2 values for class1 of column1
   # x1: column2 values for class2 of column1
   
   test_stat, pvalue = shapiro(x1)
   test_stat, pvalue = shapiro(x2)
   test_stat, pvalue = shapiro(x3)
   ```
   
   2.2. Assumption of Homogeneity of Variance

   H0: Variances are homogeneous. (p-value >= 0.05)

   - Test assumption of homogeneity of variance for both two groups with ***levene*** function.

   ```python
   test_stat, pvalue = levene(x1, x2, x3)
   ```
   
3. Application of Hypotheses
   
   3.1. If the assumptions are met, apply one way anova (f_one_way) (parametric anova test).

   ```python
   f_oneway(x1, x2, x3)
   ```
   
   3.2. If the assumptions are not met, apply kruskal (kruskal) (non-parametric anova test).

   ```python
   kruskal(x1, x2, x3)
   ```

4. Interpret the results according to the p-value of "ttest_ind" or "mannwhitney".
   
p < 0.05: H0 is rejected, there is statistically significant difference between groups.


> CASE 5: Is there statistically significant difference between total bill averages of the weekdays? 