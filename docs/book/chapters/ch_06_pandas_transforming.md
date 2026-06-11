# 6.4. Transforming

**Nguồn web:** [https://learningds.org/ch/06/pandas_transforming.html](https://learningds.org/ch/06/pandas_transforming.html)  
**Nguồn tải:** `web-html` | `ch/06/pandas_transforming`

---

# 6.4. Transforming#
Data scientists transform dataframe columns when they need to change each value
in a feature in the same way. For example, if a feature contains heights of
people in feet, a data scientist might want to transform the heights to
centimeters. In this section, we’ll introduce apply, an operation that
transforms columns of data using a user-defined function:
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
In the baby names New York Times article, Pamela
mentions that names starting with the letter L or K became popular
after 2000. On the other hand, names starting with the letter J peaked in
popularity in the 1970s and 1980s and dropped off in popularity since. We
can verify these claims using the baby dataset.
We approach this problem using the following steps:
-
Transform the Name column into a new column that contains the first
letters of each value in Name.
-
Group the dataframe by the first letter and year.
-
Aggregate the name counts by summing.
To complete the first step, we’ll apply a function to the Name column.
## 6.4.1. Apply#
pd.Series objects contain an .apply() method that takes in a function and
applies it to each value in the series. For instance, to find the lengths of
each name, we apply the len function:
names = baby['Name']
names.apply(len)
0          4
1          4
2          6
..
2020719    6
2020720    6
2020721    5
Name: Name, Length: 2020722, dtype: int64
To extract the first letter of each name, we define a custom function and pass it
into .apply():
# The argument to the function is an individual value in the series.
def first_letter(string):
return string[0]
names.apply(first_letter)
0          L
1          N
2          O
..
2020719    V
2020720    V
2020721    W
Name: Name, Length: 2020722, dtype: object
Using .apply() is similar to using a for loop. The preceding code is roughly
equivalent to writing:
result = []
for name in names:
result.append(first_letter(name))
Now we can assign the first letters to a new column in the dataframe:
letters = baby.assign(Firsts=names.apply(first_letter))
letters
Name
Sex
Count
Year
Firsts
0
Liam
M
19659
2020
L
1
Noah
M
18252
2020
N
2
Oliver
M
14147
2020
O
...
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
V
2020720
Vertie
F
5
1880
V
2020721
Wilma
F
5
1880
W
2020722 rows × 5 columns
Note
To create a new column in a dataframe, you might also encounter this syntax:
baby['Firsts'] = names.apply(first_letter)
This mutates the baby table by adding a new column called Firsts. In the preceding
code, we use .assign(), which doesn’t mutate the baby table itself; it
creates a new dataframe instead. Mutating dataframes isn’t wrong but can be a
common source of bugs. Because of this, we’ll mostly use .assign() in this
book.
## 6.4.2. Example: Popularity of “L” Names#
Now we can use the letters dataframe to see the popularity of first letters
over time:
letter_counts = (letters
.groupby(['Firsts', 'Year'])
['Count']
.sum()
.reset_index()
)
letter_counts
Firsts
Year
Count
0
A
1880
16740
1
A
1881
16257
2
A
1882
18790
...
...
...
...
3638
Z
2018
55996
3639
Z
2019
55293
3640
Z
2020
54011
3641 rows × 3 columns
fig = px.line(letter_counts.loc[letter_counts['Firsts'] == 'L'],
x='Year', y='Count', title='Popularity of "L" names',
width=350, height=250)
fig.update_layout(margin=dict(t=30))
The plot shows that “L” names were popular in the 1960s, dipped in the decades
after, but have indeed resurged in popularity since 2000.
What about “J” names?
fig = px.line(letter_counts.loc[letter_counts['Firsts'] == 'J'],
x='Year', y='Count', title='Popularity of "J" names',
width=350, height=250)
fig.update_layout(margin=dict(t=30))
The NYT article says that “J” names were popular in the 1970s and ’80s. The plot
agrees and shows that they have become less popular since 2000.
## 6.4.3. The Price of Apply#
The power of .apply() is its flexibility—you can call it with any function
that takes in a single data value and outputs a single data value.
Its flexibility has a price, though. Using .apply() can be slow, since
pandas can’t optimize arbitrary functions. For example, using .apply() for
numeric calculations is much slower than using vectorized operations directly
on pd.Series objects:
%%timeit
# Calculate the decade using vectorized operators
baby['Year'] // 10 * 10
9.66 ms ± 755 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%%timeit
def decade(yr):
return yr // 10 * 10
# Calculate the decade using apply
baby['Year'].apply(decade)
658 ms ± 49.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
The version using .apply() is 30 times slower! For numeric
operations in particular, we recommend operating on pd.Series objects
directly.
In this section, we introduced data transformations.
To transform values in a dataframe, we commonly use the .apply() and
.assign() functions.
In the next section, we’ll compare dataframes with other ways to represent and
manipulate data tables.
