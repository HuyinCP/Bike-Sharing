# 8. Wrangling Files

**Nguồn web:** [https://learningds.org/ch/08/files_intro.html](https://learningds.org/ch/08/files_intro.html)  
**Nguồn tải:** `web-html` | `ch/08/files_intro`

---

# 8. Wrangling Files#
Before you can work with data in Python, it helps to understand the files that store the source of the data.
You want answers to a couple of basic questions:
-
How much data do you have?
-
How is the source file formatted?
Answers to these questions can be very helpful. For example, if your file is too large or is not formatted the way you expect, you might not be able to properly load it into a dataframe.
Although many types of structures can represent data, in this
book we primarily work with data tables, such as Pandas DataFrames and SQL
relations. (But do note that Chapter 13 examines
less-structured text data, and Chapter 14 introduces
hierarchical formats and binary files.) We focus on data tables for several reasons. Research on how to store and manipulate data tables has resulted in
stable and efficient tools for working with tables.
Plus, data in a tabular format are close
cousins of matrices, the mathematical objects of the immensely rich field of
linear algebra.
And of course, data tables are quite common.
In this chapter, we introduce typical file formats and encodings for plain text, describe measures of file size, and use Python tools to examine source files. Later in the chapter, we introduce an alternative approach for working with files: the shell interpreter. Shell commands give us
a programmatic way to get information about a file outside the Python
environment, and the shell can be very useful with big data.
Finally, we check the data table’s shape
(the number of rows and columns) and granularity
(what a row represents).
These simple checks are the starting point for cleaning and analyzing our data.
We first provide brief descriptions of the datasets that we use as examples throughout this chapter.
