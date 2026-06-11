# 6.5. How Are Dataframes Different from Other Data Representations?

**Nguồn web:** [https://learningds.org/ch/06/pandas_other_reps.html](https://learningds.org/ch/06/pandas_other_reps.html)  
**Nguồn tải:** `web-html` | `ch/06/pandas_other_reps`

---

# 6.5. How Are Dataframes Different from Other Data Representations?#
Dataframes are just one way to represent data stored in a table. In practice,
data scientists encounter many other types of data tables, like spreadsheets,
matrices, and relations. In this section, we’ll compare and contrast the
dataframe with other representations to explain why dataframes have become so
widely used for data analysis. We’ll also point out scenarios where other
representations might be more appropriate.
## 6.5.1. Dataframes and Spreadsheets#
Spreadsheets are computer applications in which users can enter data in a grid and
use formulas to perform calculations. One well-known example today is Microsoft
Excel, although spreadsheets date back to at least 1979 with VisiCalc. Spreadsheets make it easy to see and directly
manipulate data since spreadsheet formulas can automatically recalculate results whenever the data change. In contrast, dataframe code typically needs to be manually rerun when datasets are updated. These properties make spreadsheets highly popular—by a
2005 estimate, there are over 55 million spreadsheet users compared to 3
million professional programmers in industry.
Dataframes have several key advantages over spreadsheets. Writing dataframe
code in a computational notebook like Jupyter naturally produces a data
lineage. Someone who opens the notebook can see the input files for the
notebook and how the data were changed. Spreadsheets do not make a data lineage
visible; if a person manually edits data values in a cell, it can be difficult for
future users to see which values were manually edited and how they were edited.
Dataframes can handle larger datasets than spreadsheets, and users can
also use distributed programming tools to work with huge datasets that would be
very hard to load into a spreadsheet.
## 6.5.2. Dataframes and Matrices#
A matrix is a two-dimensional array of data used primarily for linear algebra
operations. In this next example, \( \mathbf{X} \) is a matrix with three rows
and two columns:
\[\begin{split}
\begin{aligned}
\mathbf{X} = \begin{bmatrix}
1 & 0 \\
0 & 4 \\
0 & 0 \\
\end{bmatrix}
\end{aligned}
\end{split}\]
Matrices are mathematical objects defined by the operators that they allow. For
instance, matrices can be added or multiplied together. Matrices also have a
transpose. These operators have very useful properties that data scientists
rely on for statistical modeling.
One important difference between a matrix and a dataframe is that when matrices are treated as
mathematical objects, they can only contain numbers.
Dataframes, on the other hand, can also have other types of data, like text.
This
makes dataframes more useful for loading and processing raw data that may
contain all kinds of data types. In practice, data scientists often load data into dataframes, then manipulate the data into matrix form.
In this book, we’ll generally use dataframes for
exploratory data analysis and data cleaning, then process the data into
matrices for machine learning models.
Note
Data scientists refer to matrices not only as mathematical objects but also as
program objects. For instance, the R programming language has a matrix
object, while in Python we could represent a matrix using a two-dimensional
numpy array. Matrices as implemented in Python and R can contain other data
types besides numbers, but they lose mathematical properties when doing so. This is
yet another example of how domains can refer to different things with the same
term.
## 6.5.3. Dataframes and Relations#
A relation is a data table representation used in database systems,
especially SQL systems like SQLite and PostgreSQL. (We cover relations and SQL
in Working with Relations Using SQL.) Relations share many similarities
with dataframes; both use rows to represent records and columns to represent
features. Both have column names, and data within a column have the same type.
One key advantage of dataframes is that they don’t require rows to represent
records and columns to represent features. Many times, raw data don’t come in a
convenient format that can directly be put into a relation. In these scenarios,
data scientists use the dataframe to load and process data since dataframes are
more flexible in this regard. Often, data scientists will load raw data into a
dataframe, then process the data into a format that can easily be stored into a
relation.
One key advantage that relations have over dataframes is that relations are
used by relational database systems like PostgreSQL that have highly
useful features for data storage and management. Consider a data scientist at a
company that runs a large social media website. The database might hold data
that is far too large to read into a pandas dataframe all at once; instead,
data scientists use SQL queries to subset and aggregate data since database
systems are more capable of handling large datasets. Also, website users
constantly make updates to their data by making posts, uploading pictures, and
editing their profile. Here, database systems let data scientists reuse their
existing SQL queries to update their analyses with the latest data rather than
having to repeatedly download large CSV files.
