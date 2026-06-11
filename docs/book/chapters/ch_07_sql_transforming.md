# 7.4. Transforming and Common Table Expressions

**Nguồn web:** [https://learningds.org/ch/07/sql_transforming.html](https://learningds.org/ch/07/sql_transforming.html)  
**Nguồn tải:** `web-html` | `ch/07/sql_transforming`

---

# 7.4. Transforming and Common Table Expressions#
In this section, we show how to call functions to transform columns of data using built-in SQL functions. We also demonstrate how to use common table expressions to build up complex queries from simpler ones. As usual, we start by loading the database:
# Set up connection to database
import sqlalchemy
db = sqlalchemy.create_engine('sqlite:///babynames.db')
## 7.4.1. SQL Functions#
SQLite provides a variety of scalar functions, or functions that transform single data
values. When called on a column of data, SQLite will apply these functions on
each value in the column. In contrast, aggregation functions like SUM and
COUNT take a column of values as input and compute a single value as output.
SQLite provides a comprehensive list of the built-in scalar functions in its online documentation. For instance, to find the number of characters in each name, we use the
LENGTH function:
query = '''
SELECT Name, LENGTH(Name)
FROM baby
LIMIT 10;
'''
pd.read_sql(query, db)
Name
LENGTH(Name)
0
Liam
4
1
Noah
4
2
Oliver
6
...
...
...
7
Lucas
5
8
Henry
5
9
Alexander
9
10 rows × 2 columns
Notice that the LENGTH function is applied to each value within the Name
column.
Note
Like aggregation functions, each implementation of SQL provides a different set
of scalar functions. SQLite has a relatively minimal set of functions, while
PostgreSQL has many more. That said, almost all SQL implementations provide some
equivalent to SQLite’s LENGTH, ROUND, SUBSTR, and LIKE functions.
Although scalar functions use the same syntax as an aggregation function, they behave differently. This
can result in confusing output if the two are mixed together in a single query:
query = '''
SELECT Name, LENGTH(Name), AVG(Count)
FROM baby
LIMIT 10;
'''
pd.read_sql(query, db)
Name
LENGTH(Name)
AVG(Count)
0
Liam
4
174.47
Here, the AVG(Name) computes the average of the entire Count column, but the output is confusing—a reader could easily think the average is related to the name Liam. For this reason, we must be careful when scalar and aggregation functions
appear together within a SELECT statement.
To extract the first letter of each name, we can use the SUBSTR function
(short for substring). As described in the documentation, the SUBSTR
function takes three arguments. The first is the input string, the second is
the position to begin the substring (1-indexed), and the third is the
length of the substring:
query = '''
SELECT Name, SUBSTR(Name, 1, 1)
FROM baby
LIMIT 10;
'''
pd.read_sql(query, db)
Name
SUBSTR(Name, 1, 1)
0
Liam
L
1
Noah
N
2
Oliver
O
...
...
...
7
Lucas
L
8
Henry
H
9
Alexander
A
10 rows × 2 columns
We can use the AS keyword to rename the column:
query = '''
SELECT *, SUBSTR(Name, 1, 1) AS Firsts
FROM baby
LIMIT 10;
'''
pd.read_sql(query, db)
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
7
Lucas
M
11281
2020
L
8
Henry
M
10705
2020
H
9
Alexander
M
10151
2020
A
10 rows × 5 columns
After calculating the first letter of each name, our analysis aims to understand the popularity of first letters over time. To do this, we want to take the output of this SQL query and use it as a single step within a longer chain of operations.
SQL provides several options to break queries into smaller steps, which is helpful in more complex analyses like this one. The most common options for doing this are to create a new relation using a CREATE TABLE statement, create a new view using CREATE VIEW, or create a temporary relation using WITH. Each of these methods have different use-cases. For simplicity, we only describe the WITH statement in this section and suggest that readers look over the SQLite documentation for details.
## 7.4.2. Multistep Queries Using a WITH Clause#
The WITH clause lets us assign a name to any SELECT query. Then we can
treat that query as though it exists as a relation in the database just for the duration of the query.
SQLite calls these temporary relations common table expressions.
For
instance, we can take the earlier query that calculates the first letter of each
name and call it letters:
query = '''
-- Create a temporary relation called letters by calculating
-- the first letter for each name in baby
WITH letters AS (
SELECT *, SUBSTR(Name, 1, 1) AS Firsts
FROM baby
)
-- Then, select the first ten rows from letters
SELECT *
FROM letters
LIMIT 10;
'''
pd.read_sql(query, db)
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
7
Lucas
M
11281
2020
L
8
Henry
M
10705
2020
H
9
Alexander
M
10151
2020
A
10 rows × 5 columns
WITH statements are very useful since they can be chained together. We can
create multiple temporary relations in a WITH statement that each perform a
bit of work on the previous result, which lets us gradually build complicated
queries a step at a time.
## 7.4.3. Example: Popularity of “L” Names#
We can use WITH statements to look at the popularity of names that start with the letter L over time. We’ll group the temporary letters relation by the
first letter and year, then aggregate the Count column using a sum, then filter to get only names with the letter L:
query = '''
WITH letters AS (
SELECT *, SUBSTR(Name, 1, 1) AS Firsts
FROM baby
)
SELECT Firsts, Year, SUM(Count) AS Count
FROM letters
WHERE Firsts = "L"
GROUP BY Firsts, Year;
'''
letter_counts = pd.read_sql(query, db)
letter_counts
Firsts
Year
Count
0
L
1880
12799
1
L
1881
12770
2
L
1882
14923
...
...
...
...
138
L
2018
246251
139
L
2019
249315
140
L
2020
239760
141 rows × 3 columns
This relation contains the same data as the one from Chapter 6. In that chapter, we make a plot of the Count column over time, which we omit here for brevity.
In this section, we introduced data transformations.
To transform values in a relation, we commonly use SQL functions like
LENGTH() or SUBSTR().
We also explained how to build up complex queries using the WITH clause.
