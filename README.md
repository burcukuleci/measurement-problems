# MEASUREMENT PROBLEMS

This repository contains Python code files and their markdown files.

***Note: The codes are from the Miuul 'Measurement Problems' course from 'Data Scientist Path'. Some parts of the codes are modified by me.***

- Clone the 'measurement-problems' repository using your terminal or git bash.

```
git clone https://github.com/burcukuleci/measurement-problems.git
```
- Download all required packages using the requirements.txt file by running the below command in the terminal.

```
pip install -r requirements.txt
```

- All required data files are in *datasets* directory. 

***Note: This README.md file provides short information for each Python file. Separate markdown files explain the code and the project in detail. Please refer to those markdown files for detailed information.***

**OUTLINE**

1. [RATING PRODUCTS](#rating-products)
2. [SORTING PRODUCTS](#sorting-products)
3. [PROJECT: IMDB Movie Scoring Sorting](#imdb-movie-scoring-sorting)
4. [SORTING REVIEWS](#sorting-reviews)
5. [AB TESTING](#ab-testing)


## RATING PRODUCTS

Calculate the rating of a product using various factors.

### PROJECT: Rating Course Using User-Based and Time-Based Weighted Average

This project provides a comprehensive approach to rating a course using various average methods. 

In this project, we use a dataset of course reviews to demonstrate different methods of calculating ratings.

**Methods** 

- **Average Rating**: Calculates the simple average of all ratings.
- **Time-Based Weighted Average**: Gives more weight to recent ratings.
- **User-Based Weighted Average**: Gives more weight to ratings from users who have made more progress in the course.
- **Combined Weighted Rating**: Combines time-based and user-based weighted averages to provide a final rating.

*The method of calculating the course rating based on both the time passed since the rating and the user's progress is more reliable.*

The script includes functionalities to calculate average ratings, time-based weighted averages, user-based weighted averages, and a combined weighted rating.

> *python file*:  [rating_products.py](rating_products.py)

- dataset: course_reviews.csv           

*md file*: [rating_products.md](rating_products.md)

## SORTING PRODUCTS

Sorting products according to the score calculated using the course rating and other factors.

**Methods:**

- **Sorting by Rating, Comment Count and Purchase Count**: Weighted sorting score
- **Bayesian Average Rating Score (BAR Score)**: Bayesian average has a better balance of rating and quantity of rating. It ensures that products with lower numbers of ratings have less weight in the ranking.
- **Hybrid Sorting**: Calculate weighted score using both "bar score" and "weighted sorting score".

> *python file*:  [sorting_products.py](sorting_products.py)

- dataset: product_sorting.csv        

*md file*: [sorting_products.md](sorting_products.md)

## IMDB Movie Scoring Sorting

Sort movies by rating using hybrid scoring method.

Then, compare the order of the top movies with IMDB rating values and movie order.

**Methods:**

- **Vote Average**: Sort movies by 'vote_average'.
- **Average Count Score**: vote_average * vote_count
- **IMDB Weighted Rating**: Use the weighted rating equation.
- **Bayesian Average Rating (BAR) Score**: : Bayesian average has a better balance of rating and quantity of rating. It ensures that products with lower numbers of ratings have less weight in the ranking.

> *python file*:  [imdb_movie.py](imdb_movie.py)

- dataset: movies_metadata.csv, imdb_ratings.csv

*md file*: [imdb_movie.md](imdb_movie.md)

## SORTING REVIEWS

In what order should product reviews be displayed?

**Methods:**

- **Up-Down Difference Score**: Substract down rating number form up rating number.
- **Average Rating Score**: Calculate up rating percentage for a review.
- **Wilson Lower Bound (WLB) Score**: Balance the ratio of up ratings with the uncertainty that comes from having a small number of observations.
- **Case Study**: Apply the methods for reviews and sort the reviews by WLB score.

Apply the methods for reviews and sort the reviews by WLB score.

> *python file*:  [sorting_reviews.py](sorting_reviews.py)

- dataset: up down vote counts for reviews.

*md file*: [sorting_reviews.md](sorting_reviews.md)

## AB TESTING

In this script different statistical test methods are applied for different datasets.

> *python file*:  [ab_testing.py](ab_testing.py)

- datasets: seeborn's 'tips', 'diabetes' & 'titanic' and course_reviews.csv

*md file*: [ab_testing.md](ab_testing.md)

***test statistics (test_stat)***: It measures the magnitude of the difference between groups.

***p-value (pvalue)***: It indicates the probability that this difference will occur randomly.

- **p < 0.05**: *There is a statistically significant difference. Reject HO.* This means that the difference between the means of the two groups is significant at the 95% confidence level. In other words, there is less than a 5% chance that this difference will occur randomly.
- **p ≥ 0.05**: *There is no statistically significant difference.* This means that the difference between the means of the two groups is not significant at the 95% confidence level.
  
***Assumptions:***

   Normal Distribution: The data of both groups must have a normal distribution.
     
   Homogeneity of Variances: It is assumed that the variances of the two groups should be equal.

- **Confidence Interval and Correlation**

Confidence interval gives an estimated range of values for the parameter with a level specified confidence level.

Correlation coefficient shows the linear relationship between two variables. The value lies between -1 and 1.

- **AB Testing (Independent Two Sample T-test)**

The t-test is used to determine whether there is a significant difference between the means of two independent groups.

**Test Steps:**

1. Establish Hypotheses

   H0: M1 = M2 -> There is no statistically significant difference between the means of the groups.
 
   H1: M1 != M2 -> There is a statistically significant difference between the means of the groups.
   
2. Assumption Checking
   
   2.1. Normality Assumption
     
   H0: Normality assumption is met. (p-value >= 0.05)

   - Test the normality for each group with ***shapiro*** function.

   2.2. Assumption of Homogeneity of Variance

   H0: Variances are homogeneous. (p-value >= 0.05)

   - Test assumption of homogeneity of variance for both two groups with ***levene*** function.
   
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

- **AB Testing (Two Sample Proportion Test)**

AB testing (Two Sample Proportion Test) is a statistical test used to determine whether there is a significant difference between the proportions of two independent groups.

This test is used to compare the success rates of the two groups for a particular event or characteristic.

The ***proportions_ztest*** function is used to compare the proportions of two independent samples.

- **ANOVA (Analysis of Variance)**

It is used to compare the averages of more than two groups.

   H0: M1 = M2 = M3 -> There is no statistically significant difference between the means of the groups.

   H1: M1 != M2 -> There is a statistically significant difference between the means of the groups.

- If the assumptions are met, apply one way anova (f_one_way) (parametric anova test).

   ```python
   f_oneway(x1, x2, x3)
   ```
   
- If the assumptions are not met, apply kruskal (kruskal) (non-parametric anova test).

   ```python
   kruskal(x1, x2, x3)
   ```