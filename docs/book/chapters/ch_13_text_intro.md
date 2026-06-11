# 13. Working with Text

**Nguồn web:** [https://learningds.org/ch/13/text_intro.html](https://learningds.org/ch/13/text_intro.html)  
**Nguồn tải:** `web-html` | `ch/13/text_intro`

---

# 13. Working with Text#
Data can reside not just as numbers but also in words: names of dog breeds,
restaurant violation descriptions, street addresses, speeches, blog posts, internet reviews, and much more.
To organize and analyze information contained in text, we often need to do some of the following tasks:
Convert text into a standard format
This is also referred to as
canonicalizing text. For example, we might need to convert characters to
lowercase, use common spellings and abbreviations, or remove punctuation and
blank spaces.
Extract a piece of text to create a feature
As an example, a string might
contain date embedded in it, and we want to pull it out from the string
to create a date feature.
Transform text into features
We might want to encode particular words or phrases as 0-1 features to indicate their presence in a string.
Analyze text
In order to compare entire documents at once, we can
transform a document into a vector of word counts.
This chapter introduces common techniques for working with text data. We
show how simple string manipulation tools are often all we need to put text in
a standard form or extract portions of strings. We also introduce regular
expressions for more general and robust pattern matching. To demonstrate these
text operations we use several examples. We first introduce these examples and describe
the work we want to do to prepare the text for analysis.
