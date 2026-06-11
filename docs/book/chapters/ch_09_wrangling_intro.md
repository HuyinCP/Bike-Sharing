# 9. Wrangling Dataframes

**Nguồn web:** [https://learningds.org/ch/09/wrangling_intro.html](https://learningds.org/ch/09/wrangling_intro.html)  
**Nguồn tải:** `web-html` | `ch/09/wrangling_intro`

---

# 9. Wrangling Dataframes#
We often need to perform preparatory work on our data before we can begin our
analysis. The amount of preparation can vary widely, but there are a few basic steps
to move from raw data to data ready for analysis. Chapter 8
addressed the initial steps of creating a dataframe from a plain-text
source. In this chapter, we assess quality. To do this, we perform validity checks on individual data
values and entire columns. In addition to checking the quality of the data, we determine
whether or not the data need to be transformed and reshaped to get ready for
analysis. Quality checking (and fixing) and transformation are often cyclical:
the quality checks point us toward transformations we need to make, and when we
check the transformed columns to confirm that our data are ready for analysis,
we may discover they need further cleaning.
Depending on the data source, we often have different expectations for quality.
Some datasets require extensive wrangling to get them into an analyzable form,
and others arrive clean and we can quickly launch into modeling. Here
are some examples of data sources and how much wrangling we might expect to do:
-
Data from a scientific experiment or study  are typically clean,
are well documented, and have a simple structure. These data are organized to be
broadly shared so that others can build on or reproduce the findings.  They
are typically ready for analysis after little to no wrangling.
-
Data from government surveys often come with very detailed codebooks and metadata describing how the data are collected and formatted, and these datasets
are also typically ready for exploration and analysis right out of the “box.”
-
Administrative data can be clean, but without inside knowledge of the source,
we may need to extensively check their quality. Also, since we often
use these data for a purpose other than why they were collected in the first place, we
may need to transform features or combine data tables.
-
Informally collected data, such as data scraped from the web, can be quite
messy and tends to come with little documentation. For example, texts,
tweets, blogs, and Wikipedia tables. usually require formatting and cleaning
to transform them into information ready for analysis.
In this chapter, we break down data wrangling into the following stages: assess data quality; handle missing values; transform features; and reshape the data by modifying its structure and granularity. An important step in assessing the quality of the data is to consider its scope. Data scope was covered in Chapter 2, and we refer you there for a fuller treatment of the topic.
To clean and prepare data, we also rely on exploratory data analysis, especially visualizations. In this chapter, however, we focus on data wrangling and cover these other, related topics in more detail in Chapters 10 and 11.
We use the datasets introduced in Chapter 8: the DAWN government survey of emergency room visits related to drug abuse; and the San Francisco administrative data on food safety inspections of restaurants. But we begin by introducing the various data wrangling concepts through another example that is simple enough and clean enough that we can limit our focus in each of the wrangling steps.
