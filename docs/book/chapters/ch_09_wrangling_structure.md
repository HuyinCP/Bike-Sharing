# 9.5. Modifying Structure

**Nguồn web:** [https://learningds.org/ch/09/wrangling_structure.html](https://learningds.org/ch/09/wrangling_structure.html)  
**Nguồn tải:** `web-html` | `ch/09/wrangling_structure`

---

# 9.5. Modifying Structure#
If a dataframe has an inconvenient structure, it can be difficult to do the
analysis that we want. The wrangling process often reshapes the dataframe in
some way to make the analysis easier and more natural. These changes can simply
take a subset of the rows and/or columns from the table or change the table’s
granularity in a more fundamental way. In this section, we use the techniques from
Chapter 6 to show how to modify structure in the following ways:
Simplify the structure
If a dataframe has features that are not needed
in our analysis, then we may want to drop these extraneous columns to make
handling the dataframe easier. Or if we want to focus on a particular period
of time or geographic area, we may want to take a subset of the rows
(subsetting is covered in Chapter 6).
In Chapter 8, we’ll read into
our dataframe a small set of features from the hundreds available in the DAWN
survey because we were interested in understanding the patterns of type of ER
visit by demographics of the patient. In
Chapter 10, we’ll restrict an analysis of
home sale prices to one year and
a few cities in an effort to reduce the impact of inflation and to better study
the effect of location on sale price.
Adjust the granularity
In an earlier example in this chapter,
CO2 measurements were aggregated from monthly averages to yearly averages in order to
better visualize annual trends. In the next section, we provide another example
where we aggregate violation-level data to the inspection level so that it can
be combined with the restaurant inspection scores. In both of these examples, we adjust
the granularity of the dataframe to work with a coarser granularity
by grouping together records and aggregating values.
With the CO2 measurements, we grouped the monthly values from the same year and then
averaged them. Other common aggregations of a group are the number of records,
sum, minimum, maximum, and first or last value in the group. The details
of adjusting granularity of pandas dataframes can be found in
Chapter 6, including how to group by multiple column values.
Address mixed granularity
At times, a dataset might have mixed granularity, where records are at different
levels of detail. A common case is in data provided by government agencies
where data at the county and state levels are included in the same file. When
this happens, we usually want to split the dataframe into two, one at the
county level and the other at the state level. This makes county-level and
state-level analyses much easier, even feasible, to perform.
Reshape the structure
Data, especially from government sources, can be shared as pivot
tables. These wide tables have data values as column names and are often
difficult to use in analysis. We may need to reshape them into a long
form. Figure 9.2 depicts the same data stored in both
wide and long data tables.  Each row of the wide data table maps to three rows in the long data table, as highlighted in the tables. Notice that in the wide data table, each row has three values, one for each month. In the long data table, each row only has a value for one month. Long data tables are generally easier to aggregate for future analysis. Because of this, long-form data is also frequently called tidy data.
Fig. 9.2 An example of a wide data table (top) and a long data table (bottom) containing the same data#
To demonstrate reshaping, we can put the CO2 data into a wide dataframe that is like a pivot table in shape. There is a column for each month and a row for each year:
co2_pivot = pd.pivot_table(
co2[10:34],
index='Yr',   # Column to turn into new index
columns='Mo',  # Column to turn into new columns
values='Avg') # Column to aggregate
co2_wide = co2_pivot.reset_index()
display_df(co2_wide, cols=10)
Mo
Yr
1
2
3
4
...
8
9
10
11
12
0
1959
315.62
316.38
316.71
317.72
...
314.80
313.84
313.26
314.8
315.58
1
1960
316.43
316.97
317.58
319.02
...
315.91
314.16
313.83
315.0
316.19
2 rows × 13 columns
The column headings are months, and the cell values in the grid are the CO2 monthly averages. We can turn this dataframe back into a long, aka tall, dataframe, where the column names become a feature, called month, and the values in the grid are reorganized into a second feature, called average:
co2_long = co2_wide.melt(id_vars=['Yr'],
var_name='month',
value_name='average')
display_df(co2_long, rows=4)
Yr
month
average
0
1959
1
315.62
1
1960
1
316.43
...
...
...
...
22
1959
12
315.58
23
1960
12
316.19
24 rows × 3 columns
Notice that the data has been recaptured in its original shape (although the
rows are not in their original order). Wide-form data is more common when we
expect readers to look at the data table itself, like in an economics article
or news story. But long-form data is more useful for data analysis. For
instance, co2_long lets us write short pandas code to group by either year
or month, while the wide-form data makes it difficult to group by year.
The .melt() method is particularly useful for converting wide-form into long-form data.
These structural modifications have focused on a single table. However, we often want to combine information that is spread across multiple tables. In the next section, we combine the techniques introduced in this chapter to wrangle the restaurant inspection data and address joining tables.
