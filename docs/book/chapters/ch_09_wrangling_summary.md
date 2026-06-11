# 9.7. Summary

**Nguồn web:** [https://learningds.org/ch/09/wrangling_summary.html](https://learningds.org/ch/09/wrangling_summary.html)  
**Nguồn tải:** `web-html` | `ch/09/wrangling_summary`

---

# 9.7. Summary#
Data wrangling is an essential part of data analysis. Without it, we risk overlooking problems in data that can have major consequences for our future analysis. This chapter covered several important data wrangling steps that we use in nearly every analysis.
We described what to look for in a dataset after we’ve read it into a dataframe. Quality checks help us spot problems in the data. To find bad and missing values, we can take many approaches:
-
Check summary statistics, distributions, and value counts. Chapter 10 provides examples and guidance on how to go about checking the quality of your data using visualizations and summary statistics. We briefly mentioned a few approaches here. A table of counts of unique values in a feature can uncover unexpected encodings and lopsided distributions, where one option is a rare occurrence. Percentiles can be helpful in revealing the proportion of values with unusually high (or low) values.
-
Use logical expressions to identify records with values that are out of range or relationships that are out of wack. Simply computing the number of records that do not pass the quality check can quickly reveal the size of the problem.
-
Examine the whole record for those records with problematic values in a particular feature. At times, an entire record is garbled when, for example, a comma is misplaced in a CSV-formatted file. Or the record might represent an unusual situation (such as ranches being included in data on house sales), and you will need to decide whether it should be included in your analysis.
-
Refer to an external source to figure out if there’s a reason for the anomaly.
The biggest takeaway for this chapter is to be curious about your data. Look for clues that can reveal the quality of your data. The more evidence you find, the more confidence you will have in your findings. And if you uncover problems, dig deeper. Try to understand and explain any unusual phenomena. A good understanding of your data will help you assess whether an issue that you found is small and can be ignored or corrected, or whether it poses a serious limitation on the usefulness of your data.
This curiosity mindset is closely connected to exploratory data analysis, the topic of the next chapter.
