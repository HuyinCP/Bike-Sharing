# 8.7. Summary

**Nguồn web:** [https://learningds.org/ch/08/files_summary.html](https://learningds.org/ch/08/files_summary.html)  
**Nguồn tải:** `web-html` | `ch/08/files_summary`

---

# 8.7. Summary#
Data wrangling is an essential part of data analysis. Without it, we risk overlooking problems in data that can have major consequences for future analysis. This chapter covered an important first step in data wrangling: reading data from a plain-text source file into a Python dataframe and identifying its granularity. We introduced different types of file formats and encodings, and we wrote code that can read data from these formats. We checked the size of source files and considered alternative tools for working with large datasets.
We also introduced command-line tools as an alternative to Python for checking the format, encoding, and size of a file. These CLI tools are especially handy for filesystem-oriented tasks because of their simple syntax.
We’ve only touched the surface of what CLI tools can do.
In practice, the shell is capable of sophisticated data processing and
is well worth learning.
Understanding the shape and granularity of a table gives us insight into what a row in a data table represents. This helps us determine whether the granularity is mixed, aggregation is needed, or weights are required. After looking at the granularity of your dataset, you should have answers to the following questions:
-
What does a record represent? Clarity on this will help you correctly carry out a data analysis and state your findings.
-
Do all records in a table capture granularity at the same level? Sometimes a table contains additional summary rows that have a different granularity, and you want to use only those rows that are at the right level of detail.
-
If the data are aggregated, how was the aggregation performed? Summing and averaging are common types of aggregation. With averaged data, the variability in the measurements is typically reduced and relationships often appear stronger.
-
What kinds of aggregations might you perform on the data? Aggregations might be useful or necessary to combine one data table with another.
Knowing your table’s granularity is a first step to cleaning your data, and it informs you of how to analyze the data. For example, we saw the granularity of the DAWN survey is an ER visit. That naturally leads us to think about comparisons of patient demographics to the US as a whole.
The wrangling techniques in this chapter help us bring data from a source file into a dataframe and understand its structure. Once we have a dataframe, further wrangling is needed to assess and improve quality and prepare the data for analysis. We cover these topics in the next chapter.
