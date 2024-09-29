#####################################################
# AB Test for Comparing Bidding Methods Conversion
#####################################################

#####################################################
# Business Problem
#####################################################

# Facebook recently introduced a new bidding type called "average bidding" as an alternative to the existing
# "maximum bidding." One of our clients, bombabomba.com, decided to test this new feature and wants to determine
# if average bidding brings more conversions compared to maximum bidding through an A/B test.
# The A/B test has been running for 1 month, and now bombabomba.com expects you to analyze the results.
# The ultimate success metric for bombabomba.com is "Purchase." Therefore, statistical tests should focus on the Purchase metric.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


#####################################################
# Dataset Information
#####################################################

# This dataset contains information about a company's website, including the number of ads displayed and clicked,
# as well as the resulting revenue. There are two separate datasets for the Control and Test groups.
# These datasets are available on separate sheets in the "ab_testing.xlsx" file. Maximum Bidding is applied to the
# Control group, and Average Bidding is applied to the Test group.

# impression: Number of ad impressions
# Click: Number of clicks on the displayed ads
# Purchase: Number of products purchased after clicking ads
# Earning: Earnings from purchased products

#####################################################
# Project Tasks
#####################################################

######################################################
# AB Testing (Independent Two-Sample T-Test)
######################################################

# 1. Define Hypotheses
# 2. Assumption Checks
#   - 1. Normality Assumption (Shapiro test)
#   - 2. Variance Homogeneity (Levene test)
# 3. Apply the Hypothesis Test
#   - 1. If assumptions are met, perform an independent two-sample t-test
#   - 2. If assumptions are not met, use the Mann-Whitney U test
# 4. Interpret the results based on the p-value
# Note:
# - If normality is not satisfied, proceed directly to step 2.
# - If variance homogeneity is not satisfied, include an argument in step 1.

#####################################################
# Task 1: Data Preparation and Analysis
#####################################################

# Step 1: Read the dataset containing control and test group data from "ab_testing_data.xlsx" and assign them to separate variables.

control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

# Step 2: Analyze the control and test group data.

test.describe().T
control.describe().T

# Step 3: After the analysis, use the concat method to combine the control and test group data.

test["group"] = "test"
control["group"] = "control"
df = pd.concat([test, control])

#####################################################
# Task 2: Defining the Hypothesis for A/B Test
#####################################################

# Step 1: Define the hypothesis.
# H0: M1 = M2 (There is no significant difference between the groups)
# H1: M1 != M2 (There is a significant difference between the groups)

# Step 2: Analyze the mean of the "Purchase" metric for the control and test groups.

df.groupby("group").agg({"Purchase": "mean"})

#####################################################
# Task 3: Performing the Hypothesis Test
#####################################################

######################################################
# AB Testing (Independent Two-Sample T-Test)
######################################################

# Step 1: Before performing the hypothesis test, conduct assumption checks for normality and variance homogeneity.
# Test whether the control and test groups meet the normality assumption separately using the Purchase variable.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Normal distribution assumption is met

test_stat, pvalue = levene(df.loc[df["group"] == "test", "Purchase"],
                           df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Step 2: Choose the appropriate test based on the results of the Normality Assumption and Variance Homogeneity.

# Independent two-sample t-test

# Step 3: Based on the p_value from the test result, interpret whether there is a statistically significant difference
# in purchase averages between the control and test groups.

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "test", "Purchase"],
                              df.loc[df["group"] == "control", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

##############################################################
# Task 4: Analysis of the Results
##############################################################

# Step 1: Specify which test you used and the reasons for it.

# After checking for normality and confirming that both groups follow a normal distribution,
# an independent two-sample t-test was conducted to compare the purchase data of two independent groups.
# The test was executed with equal_var=True configuration after verifying the assumption of variance homogeneity.

# Step 2: Provide recommendations to the client based on the test results.

# According to the results, the average purchase amount of the test group is higher than that of the control group.
# However, the t-test results indicate that this difference is not statistically significant.
# It is recommended to repeat the test with a larger and appropriate sample size to ensure reliable results.
