# 7.3. Joining

**Nguồn web:** [https://learningds.org/ch/07/sql_joining.html](https://learningds.org/ch/07/sql_joining.html)  
**Nguồn tải:** `web-html` | `ch/07/sql_joining`

---

# 7.3. Joining#
To connect records between two data tables, SQL relations can be joined together similar to dataframes. In this section, we introduce SQL joins to replicate our analysis of the baby names data. Recall that Chapter 6 mentions a New York Times article that talks about how certain name categories, like mythological and baby boomer names, have become more or less popular over time.
We’ve taken the names and categories in the NYT article and put them in a small relation named nyt:
# Set up connection to database
import sqlalchemy
db = sqlalchemy.create_engine('sqlite:///babynames.db')
query = '''
SELECT *
FROM nyt;
'''
pd.read_sql(query, db)
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
Note
Notice that the preceding code runs a query on babynames.db, the same database
that contains the larger baby relation from the previous sections. SQL
databases can hold more than one relation, making them very useful when we need
to work with many data tables at once. CSV files, on the other hand, typically
contain one data table each—if we perform a data analysis that uses 20
data tables, we might need to keep track of the names, locations, and versions
of 20 CSV files. Instead, it could be simpler to store all the data tables
in a SQLite database stored in a single file.
To see how popular the categories of names are, we join the nyt relation with
the baby relation to get the name counts from baby.
## 7.3.1. Inner Joins#
As in Chapter 6, we’ve made smaller versions of the baby and nyt tables so that it’s easier to
see what happens when we join tables together. The relations are called
baby_small and nyt_small:
query = '''
SELECT *
FROM baby_small;
'''
pd.read_sql(query, db)
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
query = '''
SELECT *
FROM nyt_small;
'''
pd.read_sql(query, db)
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
To join relations in SQL, we use the INNER JOIN clause to say which tables we want to join and the ON clause to specify a predicate for joining the tables. Here’s an example:
query = '''
SELECT *
FROM baby_small INNER JOIN nyt_small
ON baby_small.Name = nyt_small.nyt_name
'''
pd.read_sql(query, db)
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
Notice that this result is the same as doing an inner join in pandas: the new table has the columns of both the baby_small and nyt_small
tables. The rows with the name Noah are gone, and the remaining rows have their matching category from nyt_small.
To join two tables together, we tell SQL the column(s) from each
table that we want to use to  do the join using a predicate with the ON keyword.
SQL matches rows together when the values in the joining columns fulfill the predicate, as
shown in Fig. 7.2.
Fig. 7.2 Joining two tables together with SQL#
Unlike pandas, SQL gives more flexibility on how rows are joined. The pd.merge() method can only join using simple equality, but the predicate in the ON clause can be arbitrarily complex. As an example, we take advantage of this extra versatility in Section 12.2.
## 7.3.2. Left and Right Joins#
Like pandas, SQL also supports left joins. Instead of saying INNER JOIN, we use LEFT JOIN:
query = '''
SELECT *
FROM baby_small LEFT JOIN nyt_small
ON baby_small.Name = nyt_small.nyt_name
'''
pd.read_sql(query, db)
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
None
None
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
None
None
As we might expect, the “left” side of the join refers to the table that appears on the left side of the LEFT JOIN keyword.
We can see the Noah rows are kept in the resulting relation even when they don’t have a match in the righthand relation.
Note that SQLite doesn’t support
right joins directly, but we can perform the same join by swapping the order of relations, then using LEFT JOIN:
query = '''
SELECT *
FROM nyt_small LEFT JOIN baby_small
ON baby_small.Name = nyt_small.nyt_name
'''
pd.read_sql(query, db)
nyt_name
category
Name
Sex
Count
Year
0
Karen
boomer
Karen
F
325.0
2020.0
1
Karen
boomer
Karen
M
6.0
2020.0
2
Julius
mythology
Julius
M
960.0
2020.0
3
Freya
mythology
None
None
NaN
NaN
SQLite doesn’t have a built-in keyword for outer joins. In cases where
an outer join is needed, we have to either use a different SQL engine or perform an outer join via pandas. However, in our (the authors’) experience, outer joins are rarely used in practice compared to inner and left joins.
## 7.3.3. Example: Popularity of NYT Name Categories#
Now let’s return to the full baby and nyt relations.
We want to know how the popularity of name categories in nyt has changed
over time. To answer this question, we should:
-
Inner join baby with nyt, matching rows where the names are equal.
-
Group the table by category and Year.
-
Aggregate the counts using a sum:
query = '''
SELECT
category,
Year,
SUM(Count) AS count           -- [3]
FROM baby INNER JOIN nyt        -- [1]
ON baby.Name = nyt.nyt_name   -- [1]
GROUP BY category, Year         -- [2]
'''
cate_counts = pd.read_sql(query, db)
cate_counts
category
Year
count
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
The numbers in square brackets ([1], [2], [3]) in the preceding query show how each step in our plan maps to the parts of the SQL query. The code re-creates the dataframe from Chapter 6, where we created plots to verify the claims of the New York Times article. For brevity, we omit duplicating the plots here.
Note
Notice that in the SQL code in this example, the numbers appear out of order—[3], [1], then [2]. As a rule of thumb for first-time SQL learners, we can often think of the SELECT statement as the last piece of the query to execute even though it appears first.
In this section, we introduced joins for relations. When joining relations together, we match rows using the INNER JOIN or LEFT JOIN keyword and a boolean predicate. In the next section, we’ll explain how to transform values in a relation.
