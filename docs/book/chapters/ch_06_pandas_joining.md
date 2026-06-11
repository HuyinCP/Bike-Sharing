# 6.3. Joining

**Nguồn web:** [https://learningds.org/ch/06/pandas_joining.html](https://learningds.org/ch/06/pandas_joining.html)  
**Nguồn tải:** `web-html` | `ch/06/pandas_joining`

---

# 6.3. Joining#
Data scientists very frequently want to join two or more dataframes together
in order to connect data values across dataframes. For instance, an online
bookstore might have one dataframe with the books each user has ordered and a
second dataframe with the genres of each book. By joining the two dataframes
together, the data scientist can see what genres each user prefers.
We’ll continue looking at the baby names data. We’ll use joins to check some
trends mentioned in the New York Times article about baby names. The article talks about how certain categories of
names have become more or less popular over time. For instance, it mentions
that mythological names like Julius and Cassius have become popular, while baby
boomer names like Susan and Debbie have become less popular. How has the
popularity of these categories changed over time?
We’ve taken the names and categories in the NYT article and put them in a small
dataframe:
nyt = pd.read_csv('nyt_names.csv')
nyt
nyt_name
category
0
Lucifer
forbidden
1
Lilith
forbidden
2
Danger
forbidden
...
...
...
20
Venus
celestial
21
Celestia
celestial
22
Skye
celestial
23 rows × 2 columns
To see how popular the categories of names are, we join the nyt dataframe
with the baby dataframe to get the name counts from baby:
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
For intuition, we can imagine going down each row in baby and asking: is this name in the nyt table? If so, then add the value in the category column to the row. This is the basic idea behind a join. Let’s look at a few examples on smaller dataframes first.
## 6.3.1. Inner Joins#
We start by making smaller versions of the baby and nyt tables so that it’s easier to see what happens when we join tables together:
nyt_small
nyt_name
category
0
Karen
boomer
1
Julius
mythology
2
Freya
mythology
baby_small
Name
Sex
Count
Year
0
Noah
M
18252
2020
1
Julius
M
960
2020
2
Karen
M
6
2020
3
Karen
F
325
2020
4
Noah
F
305
2020
To join tables in pandas, we’ll use the .merge() method:
baby_small.merge(nyt_small,
left_on='Name',        # column in left table to match
right_on='nyt_name')   # column in right table to match
Name
Sex
Count
Year
nyt_name
category
0
Julius
M
960
2020
Julius
mythology
1
Karen
M
6
2020
Karen
boomer
2
Karen
F
325
2020
Karen
boomer
Notice that the new table has the columns of both the baby_small and nyt_small
tables. The rows with the name Noah are gone. And the remaining rows have their
matching category from nyt_small.
Note
Readers should also be aware that pandas has a .join() method for joining two dataframes together. However, the .merge() method has more flexibility for how the dataframes are joined, which is why we focus on .merge(). We encourage readers to consult the pandas documentation for the exact difference between the two.
When we join two tables together, we tell pandas the column(s) from each
table that we want to use to make the join (the left_on and right_on arguments).
pandas matches rows together when the values in the joining columns match, as
shown in Fig. 6.4.
Fig. 6.4 To join, pandas matches rows using the values in the Name and nyt_name
columns, dropping rows that don’t have matching values#
By default, pandas does an inner join. If either table has rows that don’t
have matches in the other table, pandas drops those rows from the result. In
this case, the Noah rows in baby_small don’t have matches in
nyt_small, so they are dropped. Also, the Freya row in nyt_small
doesn’t have matches in baby_small, so it’s dropped as well. Only the
rows with a match in both tables stay in the final result.
## 6.3.2. Left, Right, and Outer Joins#
We sometimes want to keep rows without a match instead of dropping them
entirely. There are other types of joins—left, right, and outer—that keep
rows even when they don’t have a match.
In a left join, rows in the left table without a match are kept in the final
result, as shown in Fig. 6.5.
Fig. 6.5 In a left join, rows in the left table that don’t have matching values are kept#
To do a left join in pandas, use how='left' in the call to .merge():
baby_small.merge(nyt_small,
left_on='Name',
right_on='nyt_name',
how='left')           # left join instead of inner
Name
Sex
Count
Year
nyt_name
category
0
Noah
M
18252
2020
NaN
NaN
1
Julius
M
960
2020
Julius
mythology
2
Karen
M
6
2020
Karen
boomer
3
Karen
F
325
2020
Karen
boomer
4
Noah
F
305
2020
NaN
NaN
Notice that the Noah rows are kept in the final table. Since those rows didn’t
have a match in the nyt_small dataframe, the join leaves NaN values in the
nyt_name and category columns. Also, notice that the Freya row in
nyt_small is still dropped.
A right join works similarly to the left join, except that nonmatching rows
in the right table are kept instead of the left table:
baby_small.merge(nyt_small,
left_on='Name',
right_on='nyt_name',
how='right')
Name
Sex
Count
Year
nyt_name
category
0
Karen
M
6.0
2020.0
Karen
boomer
1
Karen
F
325.0
2020.0
Karen
boomer
2
Julius
M
960.0
2020.0
Julius
mythology
3
NaN
NaN
NaN
NaN
Freya
mythology
Finally, an outer join keeps rows from both tables even when they don’t have
a match:
baby_small.merge(nyt_small,
left_on='Name',
right_on='nyt_name',
how='outer')
Name
Sex
Count
Year
nyt_name
category
0
Noah
M
18252.0
2020.0
NaN
NaN
1
Noah
F
305.0
2020.0
NaN
NaN
2
Julius
M
960.0
2020.0
Julius
mythology
3
Karen
M
6.0
2020.0
Karen
boomer
4
Karen
F
325.0
2020.0
Karen
boomer
5
NaN
NaN
NaN
NaN
Freya
mythology
## 6.3.3. Example: Popularity of NYT Name Categories#
Now let’s return to the full dataframes baby and nyt:
# .head() slices out the first few rows - convenient for saving space
baby.head(2)
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
nyt.head(2)
nyt_name
category
0
Lucifer
forbidden
1
Lilith
forbidden
We want to know how the popularity of name categories in nyt has changed
over time. To answer this question:
-
Inner join baby with nyt.
-
Group the table by category and Year.
-
Aggregate the counts using a sum:
cate_counts = (
baby.merge(nyt, left_on='Name', right_on='nyt_name') # [1]
.groupby(['category', 'Year'])                       # [2]
['Count']                                            # [3]
.sum()                                               # [3]
.reset_index()
)
cate_counts
category
Year
Count
0
boomer
1880
292
1
boomer
1881
298
2
boomer
1882
326
...
...
...
...
647
mythology
2018
2944
648
mythology
2019
3320
649
mythology
2020
3489
650 rows × 3 columns
Now we can plot the popularity of boomer names and mythology names:
boomers = px.line(cate_counts.query('category == "boomer"'),
x='Year', y='Count')
myths = px.line(cate_counts.query('category == "mythology"'),
x='Year', y='Count')
fig = left_right(boomers, myths, width=500, height=200,
subplot_titles=['Boomer names', 'Mythology names'])
margin(fig, t=30)
fig
As the NYT article claims, baby boomer names have become less popular since
2000, while mythology names have become more popular.
We can also plot the popularities of all the categories
at once. Take a look at the following plots and see whether
they support the claims made in the New York Times article:
fig = px.line(cate_counts, x='Year', y='Count',
facet_col='category', facet_col_wrap=3,
facet_row_spacing=0.15,
width=600, height=400)
margin(fig, t=30)
fig.update_yaxes(matches=None, showticklabels=False)
In this section, we introduced joins for dataframes.
When joining dataframes together, we match rows using the .merge() function.
It’s important to consider the type of join (inner, left, right, or outer)
when joining dataframes.
In the next section, we’ll explain how to transform values in a dataframe.
