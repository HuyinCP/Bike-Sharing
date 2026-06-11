# 7.2. Aggregating

**Nguồn web:** [https://learningds.org/ch/07/sql_aggregating.html](https://learningds.org/ch/07/sql_aggregating.html)  
**Nguồn tải:** `web-html` | `ch/07/sql_aggregating`

---

# 7.2. Aggregating#
This section introduces grouping and aggregating in SQL.
We’ll work with the baby names data, as in the previous section:
import sqlalchemy
db = sqlalchemy.create_engine('sqlite:///babynames.db')
query = '''
SELECT *
FROM baby
LIMIT 10
'''
pd.read_sql(query, db)
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
7
Lucas
M
11281
2020
8
Henry
M
10705
2020
9
Alexander
M
10151
2020
10 rows × 4 columns
## 7.2.1. Basic Group-Aggregate Using GROUP BY#
Let’s say we want to find out the total number of babies born as recorded in
this data. This is simply the sum of the Count column. SQL provides
functions that we use in the SELECT statement, like SUM:
query = '''
SELECT SUM(Count)
FROM baby
'''
pd.read_sql(query, db)
SUM(Count)
0
352554503
In Chapter 6, we used grouping and aggregation to figure out whether US births are trending upward over time. We grouped the dataset by year using .groupby(), then summed the counts within each group using .sum().
In SQL, we instead group using the GROUP BY clause, then call aggregation functions in SELECT:
query = '''
SELECT Year, SUM(Count)
FROM baby
GROUP BY Year
'''
pd.read_sql(query, db)
Year
SUM(Count)
0
1880
194419
1
1881
185772
2
1882
213385
...
...
...
138
2018
3487193
139
2019
3437438
140
2020
3287724
141 rows × 2 columns
As with dataframe grouping, notice that the Year column contains the unique Year values—there are no duplicate Year values anymore since we grouped them together. When grouping in pandas, the grouping columns become the index of the resulting dataframe. However, relations don’t have row labels, so the Year values are just a column in the resulting relation.
Here’s the basic recipe for grouping in SQL:
SELECT
col1,           -- column used for grouping
SUM(col2)       -- aggregation of another column
FROM table_name   -- relation to use
GROUP BY col1     -- the column(s) to group by
Note that the order of clauses in a SQL statement is important. To avoid a syntax error, SELECT needs to appear first, then FROM, then WHERE, then GROUP BY.
When using GROUP BY we need to be careful about the columns given to SELECT. In general, we can only include columns without an aggregation when we use those columns to group. For instance, in the preceding example we grouped by the Year column, so we can include Year in the SELECT clause. All other columns included in SELECT should be aggregated, as we did earlier with SUM(Count). If we included a “bare” column like Name that wasn’t used for grouping, it’s ambiguous which name within the group should be returned. Although bare columns won’t cause an error for SQLite, they cause other SQL engines to error, so we recommend avoiding them.
## 7.2.2. Grouping on Multiple Columns#
We pass multiple columns into GROUP BY to group by multiple columns at
once. This is useful when we need to further subdivide our groups. For
example, we can group by both year and sex to see how many male and female
babies were born over time:
query = '''
SELECT Year, Sex, SUM(Count)
FROM baby
GROUP BY Year, Sex
'''
pd.read_sql(query, db)
Year
Sex
SUM(Count)
0
1880
F
83929
1
1880
M
110490
2
1881
F
85034
...
...
...
...
279
2019
M
1785527
280
2020
F
1581301
281
2020
M
1706423
282 rows × 3 columns
Notice that the preceding code is very similar to grouping by a single column, except that it gives multiple columns to GROUP BY to group by both Year and Sex.
Note
Unlike pandas, SQLite doesn’t provide a simple way to pivot a relation.
Instead, we can use GROUP BY on two columns in SQL, read the result into a
dataframe, and then use the unstack() dataframe method.
## 7.2.3. Other Aggregation Functions#
SQLite has several other built-in aggregation functions besides SUM, such as
COUNT, AVG, MIN, and MAX. For the full list of functions, consult the
SQLite website.
To use another aggregation function, we call it in the SELECT clause. For
instance, we can use MAX instead of SUM:
query = '''
SELECT Year, MAX(Count)
FROM baby
GROUP BY Year
'''
pd.read_sql(query, db)
Year
MAX(Count)
0
1880
9655
1
1881
8769
2
1882
9557
...
...
...
138
2018
19924
139
2019
20555
140
2020
19659
141 rows × 2 columns
Note
The built-in aggregation functions are one of the first places a data
scientist may encounter differences in SQL implementations. For instance,
SQLite has a relatively minimal set of aggregation functions while PostgreSQL
has many more. That said, almost all SQL implementations provide SUM, COUNT,
MIN, MAX, and AVG.
This section covered common ways to aggregate data in SQL using
the GROUP BY keyword with one or more columns.
In the next section, we’ll explain how to join relations together.
