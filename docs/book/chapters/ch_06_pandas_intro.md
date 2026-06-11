# 6. Working with Dataframes Using pandas

**Nguồn web:** [https://learningds.org/ch/06/pandas_intro.html](https://learningds.org/ch/06/pandas_intro.html)  
**Nguồn tải:** `web-html` | `ch/06/pandas_intro`

---

# 6. Working with Dataframes Using pandas#
Data scientists work with data stored in tables. This chapter introduces
dataframes, one of the most widely used ways to represent data tables. We
also introduce pandas, the standard Python package for working with
dataframes. Here is an example of a dataframe that holds information about
popular dog breeds:
grooming
food_cost
kids
size
breed
Labrador Retriever
weekly
466.0
high
medium
German Shepherd
weekly
466.0
medium
large
Beagle
daily
324.0
high
small
Golden Retriever
weekly
466.0
high
medium
Yorkshire Terrier
daily
324.0
low
small
Bulldog
weekly
466.0
medium
medium
Boxer
weekly
466.0
high
medium
In a dataframe, each row represents a single record—in this case, a single
dog breed. Each column represents a feature about the record—for example, the
grooming column represents how often each dog breed needs to be groomed.
Dataframes have labels for both columns and rows. For instance, this dataframe
has a column labeled grooming and a row labeled German Shepherd. The
columns and rows of a dataframe are ordered—we can refer to the Labrador
Retriever row as the first row of the dataframe.
Within a column, data have the same type. For instance, the the cost of food
contains numbers, and the  size of the dog consists of categories. But data types can
be different within a row.
Because of these properties, dataframes enable all sorts of useful operations.
Note
Data scientists often find themselves working with people from
different backgrounds who use different terms. For instance, computer
scientists say that the columns of a dataframe represent features of the
data, while statisticians call them variables instead.
Other times, people use the same term to refer to slightly different
ideas. Data types in a programming sense refers to how a computer stores
data internally. For instance, the size column has a string data type in
Python. But from a statistical point of view, the type of the size column is ordered categorical data (ordinal data). We talk more about this specific distinction in Exploratory Data Analysis.
In this chapter, we introduce common dataframe operations using
pandas. Data scientists use the pandas library when working with dataframes
in Python. First, we explain the main objects that pandas provides: the
DataFrame and Series classes. Then we show how to use pandas to
perform common data manipulation tasks, like slicing, filtering, sorting,
grouping, and joining.
