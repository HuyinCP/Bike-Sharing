# 14. Data Exchange

**Nguồn web:** [https://learningds.org/ch/14/web_intro.html](https://learningds.org/ch/14/web_intro.html)  
**Nguồn tải:** `web-html` | `ch/14/web_intro`

---

# 14. Data Exchange#
Data can be stored and exchanged in many different formats.
Thus far, we’ve focused on
plain-text delimited and fixed-width formats (Chapter 8). In this chapter, we expand our horizons a bit and introduce a few other popular formats. While CSV, TSV, and FWF files are useful for organizing data into a data frame, other file formats can save space or represent more complex data structures. Binary files (binary is a term for formats that aren’t plain-text) can be more economical than plain-text data sources. For example, in this chapter we introduce NetCDF, a popular binary format for exchanging large amounts of scientific data. Other plain-text formats like JSON and XML can organize data in ways that are more general and useful for complex data structures. Even HTML web pages, a close cousin to XML, often contain useful information that we can scrape and wrangle into shape for analysis.
In this chapter, we introduce these popular formats, describe a mental model for their organization, and provide examples. In addition to introducing these formats, we cover programmatic ways to acquire data online. Before the internet, data scientists had to physically move disk drives to share data with one another. Now we can freely retrieve datasets from computers across the world. We introduce HTTP, the primary communication protocol for the web, and REST, an architecture to transfer data. By learning a bit about these web technologies, we can take better advantage of the web as a data source.
Throughout this book, we have set an example of reproducible code for wrangling, exploring, and modeling with data. In this chapter, we address how to acquire data that are available online in a reproducible fashion.
We begin with a description of NetCDF, followed by JSON. Then, after an overview of web protocols for data exchange, we wrap up the chapter with an introduction to XML, HTML, and XPath, a tool for extracting content from these types of files.
