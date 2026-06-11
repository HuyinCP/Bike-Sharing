# 7. Working with Relations Using SQL

**Nguồn web:** [https://learningds.org/ch/07/sql_intro.html](https://learningds.org/ch/07/sql_intro.html)  
**Nguồn tải:** `web-html` | `ch/07/sql_intro`

---

# 7. Working with Relations Using SQL#
In Working with Dataframes Using pandas, we used dataframes to represent tables of data. This chapter introduces
relations, another widely used way to represent data tables. We
also introduce SQL, the standard programming language for working with
relations. Here’s an example of a relation that holds information about
popular dog breeds:
Like dataframes, each row in a relation represents a single record—in this case, a single
dog breed. Each column represents a feature about the record—for example, the
grooming column represents how often each dog breed needs to be groomed.
Both relations and dataframes have labels for each column in the table. However, one key difference is that the rows in a relation don’t have labels, while rows in a dataframe do.
In this chapter, we demonstrate common relation operations using SQL.
We start by explaining the structure of SQL queries. Then we show how to use
SQL to perform common data manipulation tasks, like slicing, filtering,
sorting, grouping, and joining.
Note
This chapter replicates the data analyses in Working with Dataframes Using pandas using
relations and SQL instead of dataframes and Python. The datasets, data
manipulations, and conclusions are nearly identical across the two chapters for ease of comparison between performing data manipulations in pandas and SQL.
