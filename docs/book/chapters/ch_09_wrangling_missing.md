# 9.3. Missing Values and Records

**Nguồn web:** [https://learningds.org/ch/09/wrangling_missing.html](https://learningds.org/ch/09/wrangling_missing.html)  
**Nguồn tải:** `web-html` | `ch/09/wrangling_missing`

---

# 9.3. Missing Values and Records#
In Chapter 3, we considered the potential
problems when the population and the access frame are not in alignment,
so we can’t access everyone we want to study. We also described problems when
someone refuses to participate in the study. In these cases, entire
records/rows are missing, and we discussed the kinds of bias that can
occur due to missing records. If nonrespondents differ in critical ways from
respondents or if the nonresponse rate is not negligible, then our analysis may
be seriously flawed.  The example in
Chapter 3 on election polls showed that increasing the sample size without
addressing nonresponse does not reduce nonresponse bias. Also in that chapter,
we discussed ways to prevent nonresponse. These preventive measures include
using  incentives to encourage response, keeping surveys short, writing clear
questions, training interviewers, and investing in extensive follow-up
procedures. Unfortunately, despite these efforts, some amount of nonresponse is unavoidable.
When a record is not entirely missing, but a particular field in a record is
unavailable, we have nonresponse at the field level. Some datasets use a
special coding to signify that the information is missing.  We saw that the Mauna
Loa data uses -99.99 to indicate a missing CO2 measurement. We found only seven of these
values among 738 rows in the table.
In this case, we showed that these missing values have little impact on the analysis.
The values for a feature are called missing completely at random when those records with the missing data are like a randomly chosen subset of records. That is, whether or not a record has a missing value does not depend on the unobserved
feature, the values of other features, or the sampling design.
For example, if someone accidentally breaks the laboratory equipment at Manua Loa and CO2 is not
recorded for a day, there is no reason to think that the level of CO2 that day
had something to do with the lost measurements.
At other times, we consider values missing at random given covariates (covariates are other features in the dataset).
For example, the type of an ER visit in the DAWN survey is missing at random given
covariates if, say, the nonresponse depends only on race and sex (and not on the type of visit or anything else).
In these limited cases, the observed data can be weighted to accommodate for nonresponse.
In some surveys, missing information is further categorized as to whether the
respondent refused to answer, the respondent was unsure of the answer, or the interviewer
didn’t ask the question. Each of these types of missing values is recorded
using a different value. For example, according to the codebook, many questions in the DAWN survey use a
code of -7 for not applicable, -8 for not documented, and -9 for missing.
Codings such as these can help us further refine our study of nonresponse.
After nonresponse has occurred, it is sometimes possible to use models to
predict the missing data. We describe this process next.
But remember, predicting missing observations is never as good
as observing them in the first place.
At times, we substitute a reasonable value for a missing one to create a “clean”
dataframe.  This process is called imputation. Some common approaches for
imputing values are deductive, mean, and hot-deck imputation.
In deductive imputation, we fill in a value through logical relationships with other features.
For example, here is a row in the business dataframe for San Francisco restaurant
inspections. The zip code is erroneously marked as “Ca” and latitude and
longitude are missing:
bus[bus['postal_code'] == "Ca"]
business_id
name
address
city
...
postal_code
latitude
longitude
phone_number
5480
88139
TACOLICIOUS
2250 CHESTNUT ST
San Francisco
...
Ca
NaN
NaN
+14156496077
1 rows × 9 columns
We can look up the address on the USPS website to get
the correct zip code, and we can use Google Maps to find the latitude and
longitude of the restaurant to fill in these missing values.
Mean imputation uses an average value from rows in the dataset that aren’t missing.
As a simple example, if a dataset on test scores is missing scores for some students,
mean imputation would fill in the missing value using the mean of the nonmissing scores.
A key issue with mean imputation is that the variability in the imputed
feature will be smaller because the feature now has values that are identical
to the mean. This affects later analysis if not handled properly—for
instance, confidence intervals will be smaller than they should be (these topics are covered in Chapter 17).
The missing values for CO2 in Mauna Loa used a more sophisticated averaging technique that included neighboring seasonal values.
Hot-deck imputation uses a chance process to select a value at random from rows
that have values. As a simple example, hot-deck imputation could fill in
missing test scores by randomly choosing another test score in the dataset.
A potential problem with hot-deck imputation is that the strength of a
relationship between the features might weaken because we have added randomness.
For mean and hot-deck imputation, we often impute values based on other records in the
dataset that have similar values in other features.
More sophisticated imputation techniques use nearest-neighbor methods to find
similar subgroups of records and others use regression techniques to predict
the missing value.
With all of these types of imputation, we should create a new feature that
contains the altered data or a new feature to indicate whether or not the
response in the original feature has been imputed so that we can track our changes.
Decisions to keep or drop a record with a missing value, to change a value, or to remove a feature
may seem small, but they can be critical. One anomalous record can seriously
impact your findings. Whatever you decide, be sure to check the impact of
dropping or changing features and records. And be transparent and thorough in
reporting any modifications you make to the data. It’s best to make these
changes programmatically to reduce potential errors and enable others to
confirm exactly what you have done by reviewing your code.
The same transparency and reproducible precautions hold for data transformations, which we discuss next.
