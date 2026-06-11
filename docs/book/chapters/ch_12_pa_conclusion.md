# 12.7. Summary

**Nguồn web:** [https://learningds.org/ch/12/pa_conclusion.html](https://learningds.org/ch/12/pa_conclusion.html)  
**Nguồn tải:** `web-html` | `ch/12/pa_conclusion`

---

# 12.7. Summary#
In this chapter, we replicated Barkjohn’s analysis.
We created a model that corrects PurpleAir measurements
so that they closely match AQS measurements.
The accuracy of this model enables the PurpleAir sensors to be
included on official US government maps, like the AirNow Fire and Smoke map.
Importantly, this model gives people timely and accurate measurements of
air quality.
We saw how crowdsourced, open data can be improved with data from precise, rigorously maintained, government-monitored equipment. In the process, we focused on cleaning and merging data from multiple sources, but we also fit models to adjust and improve air quality measurements.
For this case study, we applied many concepts covered in this part of the book.
As you saw, wrangling files and data tables into a form we can analyze is a large and important part of data science. We used file wrangling and the notions of granularity from Chapter 8 to prepare two sources for merging. We got them into structures where we could match neighboring air quality sensors.
This “grungy” part of data science was essential to widening the reach of data from rigorously maintained, precise government-monitored equipment by augmenting it with crowd-sourced, open data.
This preparation process involved intensive, careful examination, cleaning, and improvement of the data to ensure their compatibility across the two sources and their trustworthiness in our analysis.
Concepts from Chapter 9 helped us work with time data effectively and find and correct numerous issues like missing data points and even duplicated data values.
File and data wrangling, exploratory data analysis, and visualization are major parts of many analyses.
While fitting models may seem to be the most exciting part of data science, getting to know and trust the data is crucial and often leads to important insights in the modeling phase. Topics related to modeling make up most of the rest of this book. However, before we begin, we cover two more topics related to data wrangling.
In the next chapter, we show how to create analyzable data from text, and in the following chapter we examine other formats for source files that we mentioned in Chapter 8.
Before you head to the next chapter, take stock of what you’ve learned so far.
Pat yourself on the back—you’ve already come a long way!
The principles and techniques we’ve covered here are useful for nearly
every type of data analysis, and you can readily
start applying them toward analyses of your own.
