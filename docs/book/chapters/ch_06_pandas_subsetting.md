# 6.1. Subsetting

**Nguồn web:** [https://learningds.org/ch/06/pandas_subsetting.html](https://learningds.org/ch/06/pandas_subsetting.html)  
**Nguồn tải:** `web-html` | `ch/06/pandas_subsetting`

---

# 6.1. Subsetting#
This section introduces operations for taking subsets of dataframes. When data
scientists first read in a dataframe, they often want to subset the specific
data that they plan to use. For example, a data scientist can slice out the
10 relevant features from a dataframe with hundreds of columns. Or they can
filter a dataframe to remove rows with incomplete data. For the rest of this
chapter, we demonstrate dataframe operations using a dataframe of baby names.
## 6.1.1. Data Scope and Question#
There’s a 2021 New York Times article that talks about Prince Harry and
Meghan Markle’s unique choice for their new baby daughter’s name: Lilibet. The article has an interview with Pamela Redmond,
an expert on baby names, who talks about interesting trends in how people name
their kids. For example, she says that names that start with the letter L
have become very popular in recent years, while names that start with the
letter J were most popular in the 1970s and 1980s. Are these claims reflected
in data? We can use pandas to find out.
First, we import the package as pd, the canonical abbreviation:
import pandas as pd
We have a dataset of baby names stored in a comma-separated values (CSV) file
called babynames.csv. We use the pd.read_csv function to read the file as a
pandas.DataFrame object:
baby = pd.read_csv('babynames.csv')
baby
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
2020719
Verona
F
5
1880
2020720
Vertie
F
5
1880
2020721
Wilma
F
5
1880
2020722 rows × 4 columns
The data in the baby table comes from the US Social Security Administration (SSA),
which records the baby name and birth sex for birth certificate purposes. The SSA makes the baby names data available on its website.
We’ve loaded this data into the baby table.
The SSA website has a page that describes the data in more detail. We won’t go
in depth in this chapter about the data’s limitations, but we’ll point out
this relevant information from the website:
All names are from Social Security card applications for births that occurred
in the United States after 1879. Note that many people born before 1937 never
applied for a Social Security card, so their names are not included in our
data. For others who did apply, our records may not show the place of birth,
and again their names are not included in our data.
All data are from a 100% sample of our records on Social Security card
applications as of March 2021.
It’s also important to point out that at the time of this writing, the SSA dataset only provides the binary options of male and female. We hope that in the future, national datasets like this one will provide more inclusive options.
## 6.1.2. Dataframes and Indices#
Let’s examine the baby dataframe in more detail. A dataframe has rows and
columns. Every row and column has a label, as highlighted in
Fig. 6.1.
Fig. 6.1 The baby dataframe has labels for both rows and columns (boxed)#
By default, pandas assigns row labels as incrementing numbers starting from
0. In this case, the data at the row labeled 0 and column labeled Name has
the data 'Liam'.
Dataframes can also have strings as row labels. Fig. 6.2 shows
a dataframe of dog data where the row labels are strings.
Fig. 6.2 Row labels in dataframes can also be strings, as in this example, in which each row is
labeled using the dog breed name#
The row labels have a special name. We call them the index of a dataframe,
and pandas stores the row labels in a special pd.Index object. We won’t
discuss the pd.Index object since it’s less common to manipulate the
index itself. For now, it’s important to remember that even though the index looks
like a column of data, the index really represents row labels, not data. For
instance, the dataframe of dog breeds has four columns of data, not five, since
the index doesn’t count as a column.
## 6.1.3. Slicing#
Slicing is an operation that creates a new dataframe by taking a subset of
rows or columns out of another dataframe. Think about slicing a tomato—slices
can go both vertically and horizontally. To take slices of a dataframe in
pandas, we use the .loc and .iloc properties. Let’s start with .loc.
Here’s the full baby dataframe:
baby
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
2020719
Verona
F
5
1880
2020720
Vertie
F
5
1880
2020721
Wilma
F
5
1880
2020722 rows × 4 columns
.loc lets us select rows and columns using their labels. For example, to get the data in the row labeled 1 and column labeled Name:
#        The first argument is the row label
#        ↓
baby.loc[1, 'Name']
#            ↑
#            The second argument is the column label
'Noah'
Warning
Notice that .loc needs square brackets; running baby.loc(1, 'Name') will result in an error.
To slice out multiple rows or columns, we can use Python slice syntax instead
of individual values:
baby.loc[0:3, 'Name':'Count']
Name
Sex
Count
0
Liam
M
19659
1
Noah
M
18252
2
Oliver
M
14147
3
Elijah
M
13034
To get an entire column of data, we can pass an empty slice as the first argument:
baby.loc[:, 'Count']
0          19659
1          18252
2          14147
...
2020719        5
2020720        5
2020721        5
Name: Count, Length: 2020722, dtype: int64
Notice that the output of this doesn’t look like a dataframe, and it’s not.
Selecting out a single row or column of a dataframe produces a pd.Series
object:
counts = baby.loc[:, 'Count']
counts.__class__.__name__
'Series'
What’s the difference between a pd.Series object and a pd.DataFrame object?
Essentially, a pd.DataFrame is two-dimensional—it has rows and columns and
represents a table of data. A pd.Series is one-dimensional—it represents a
list of data. pd.Series and pd.DataFrame objects have many methods in
common, but they really represent two different things. Confusing the two can
cause bugs and confusion.
To select specific columns of a dataframe, pass a list into .loc:
# Here's the original dataframe
baby
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
2020719
Verona
F
5
1880
2020720
Vertie
F
5
1880
2020721
Wilma
F
5
1880
2020722 rows × 4 columns
# And here's the dataframe with only Name and Year columns
baby.loc[:, ['Name', 'Year']]
#           └──────┬───────┘
#         list of column labels
Name
Year
0
Liam
2020
1
Noah
2020
2
Oliver
2020
...
...
...
2020719
Verona
1880
2020720
Vertie
1880
2020721
Wilma
1880
2020722 rows × 2 columns
Selecting columns is very common, so there’s a shorthand:
# Shorthand for baby.loc[:, 'Name']
baby['Name']
0            Liam
1            Noah
2          Oliver
...
2020719    Verona
2020720    Vertie
2020721     Wilma
Name: Name, Length: 2020722, dtype: object
# Shorthand for baby.loc[:, ['Name', 'Count']]
baby[['Name', 'Count']]
Name
Count
0
Liam
19659
1
Noah
18252
2
Oliver
14147
...
...
...
2020719
Verona
5
2020720
Vertie
5
2020721
Wilma
5
2020722 rows × 2 columns
Slicing using .iloc works similarly to .loc, except that .iloc uses the
positions of rows and columns rather than labels. It’s easiest to show the
difference between .iloc and .loc when the dataframe index has strings, so
for demonstration purposes, let’s look at a dataframe with information on dog
breeds:
dogs = pd.read_csv('dogs.csv', index_col='breed')
dogs
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
To get the first three rows and the first two columns by position, use .iloc:
dogs.iloc[0:3, 0:2]
grooming
food_cost
breed
Labrador Retriever
weekly
466.0
German Shepherd
weekly
466.0
Beagle
daily
324.0
The same operation using .loc requires us to use the dataframe labels:
dogs.loc['Labrador Retriever':'Beagle', 'grooming':'food_cost']
grooming
food_cost
breed
Labrador Retriever
weekly
466.0
German Shepherd
weekly
466.0
Beagle
daily
324.0
Next, we’ll look at filtering rows.
## 6.1.4. Filtering Rows#
So far, we’ve shown how to use .loc and .iloc to slice a dataframe using
labels and positions.
However, data scientists often want to filter rows—they want to take
subsets of rows using some criteria. Let’s say we want to find the most
popular baby names in 2020. To do this, we can filter rows to keep only the
rows where the Year is 2020.
To filter, we’d like to check whether each value in the Year
column is equal to 1970 and then keep only those rows.
To compare each value in Year, we slice out the column and make a boolean
comparison
(this is similar to what we’d do with a numpy array):
# Here's the dataframe for reference
baby
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
2020719
Verona
F
5
1880
2020720
Vertie
F
5
1880
2020721
Wilma
F
5
1880
2020722 rows × 4 columns
# Get a Series with the Year data
baby['Year']
0          2020
1          2020
2          2020
...
2020719    1880
2020720    1880
2020721    1880
Name: Year, Length: 2020722, dtype: int64
# Compare with 2020
baby['Year'] == 2020
0           True
1           True
2           True
...
2020719    False
2020720    False
2020721    False
Name: Year, Length: 2020722, dtype: bool
Notice that a boolean comparison on a Series gives a Series of booleans. This
is nearly equivalent to writing:
is_2020 = []
for value in baby['Year']:
is_2020.append(value == 2020)
But the boolean comparison is easier to write and much faster to execute than a
for loop.
Now we tell pandas to keep only the rows where the comparison evaluated to True:
# Passing a Series of booleans into .loc only keeps rows where the Series has
# a True value.
#        ↓
baby.loc[baby['Year'] == 2020, :]
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
31267
Zylynn
F
5
2020
31268
Zynique
F
5
2020
31269
Zynlee
F
5
2020
31270 rows × 4 columns
# Filtering has a shorthand. This computes the same table as the snippet above
# without using .loc
baby[baby['Year'] == 2020]
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
2
Oliver
M
14147
2020
...
...
...
...
...
31267
Zylynn
F
5
2020
31268
Zynique
F
5
2020
31269
Zynlee
F
5
2020
31270 rows × 4 columns
Finally, to find the most common names in 2020, sort the dataframe by Count
in descending order:
# Wrapping a long expression in parentheses lets us easily add
# line breaks to make it more readable.
(baby[baby['Year'] == 2020]
.sort_values('Count', ascending=False)
.head(7) # take the first seven rows
)
Name
Sex
Count
Year
0
Liam
M
19659
2020
1
Noah
M
18252
2020
13911
Emma
F
15581
2020
2
Oliver
M
14147
2020
13912
Ava
F
13084
2020
3
Elijah
M
13034
2020
13913
Charlotte
F
13003
2020
We see that Liam, Noah, and Emma were the most popular baby names in 2020.
## 6.1.5. Example: How Recently has Luna Become a Popular Name?#
The New York Times article mentions that the name Luna was almost nonexistent
before 2000 but has since grown to become a very popular name for girls.
When exactly did Luna become popular?
We can
check this using slicing and filtering. When approaching a data manipulation
task, we recommend breaking the problem down into smaller steps. For
example, we could think:
-
Filter: keep only rows with 'Luna' in the Name column.
-
Filter: keep only rows with 'F' in the Sex column.
-
Slice: keep the Count and Year columns.
Now it’s a matter of translating each step into code:
luna = baby[baby['Name'] == 'Luna'] # [1]
luna = luna[luna['Sex'] == 'F']     # [2]
luna = luna[['Count', 'Year']]      # [3]
luna
Count
Year
13923
7770
2020
45366
7772
2019
77393
6929
2018
...
...
...
2014083
17
1883
2018187
18
1881
2020223
15
1880
128 rows × 2 columns
In this book, we use a library called plotly for plotting.
We won’t cover plotting in depth here
since we talk more about it in Chapter 11.
For now, we use px.line() to make a simple line plot:
px.line(luna, x='Year', y='Count', width=350, height=250)
It’s just as the article says. Luna wasn’t popular at all until the year 2000
or so. In other words, if someone tells you that their name is Luna, you can
take a pretty good guess at their age even without any other information about
them!
Just for fun, here’s the same plot for the name Siri:
# Using .query is similar to using .loc with a boolean series. query() has more
# restrictions on filtering but can be convenient as a shorthand.
siri = (baby.query('Name == "Siri"')
.query('Sex == "F"'))
px.line(siri, x='Year', y='Count', width=350, height=250)
Why might the popularity have dropped so suddenly after 2010?
Well, Siri happens to be the
name of Apple’s voice assistant and was introduced in 2011.
Let’s draw a line for the year 2011 and take a look…
fig = px.line(siri, x="Year", y="Count", width=350, height=250)
fig.add_vline(
x=2011, line_color="red", line_dash="dashdot", line_width=4, opacity=0.7
)
It looks like parents don’t want their kids to be confused when other
people say “Hey Siri” to their phones.
In this section, we introduced dataframes in pandas.
We covered the common ways that data scientists subset dataframes—slicing
with labels and filtering using a boolean condition.
In the next section, we explain how to aggregate rows together.
