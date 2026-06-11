# 13.5. Summary

**Nguồn web:** [https://learningds.org/ch/13/text_summary.html](https://learningds.org/ch/13/text_summary.html)  
**Nguồn tải:** `web-html` | `ch/13/text_summary`

---

# 13.5. Summary#
This chapter introduced techniques for working with text to clean and analyze data, including string manipulation, regular expressions, and document analysis.
Text data has rich information about how people live, work, and think.
But this data is also hard for computers to use—think about all
the creative ways people manage to spell the same word.
The techniques in this chapter let us correct typos,
extract features from logs, and compare documents.
We don’t recommend you use regular expressions to:
-
Parse hierarchical structures such as JSON or HTML; use a parser instead.
-
Search for complex properties, like palindromes and balanced parentheses.
-
Validate a complex feature, such as a valid email address.
While powerful, regular expressions are terrible at these types of tasks.
However, in our experience, even the basics of text manipulation can enable all sorts of interesting analyses—a little bit goes a long way.
We have one final caution about regular expressions: they can be computationally expensive. You will want to consider the trade-offs between these concise clear expressions and the overhead they create if they’re being put into production code.
The next chapter considers other sorts of data, such as data in binary formats, and the highly structured text of JSON and HTML. Our focus will be on loading these data into dataframes and other Python data structures.
