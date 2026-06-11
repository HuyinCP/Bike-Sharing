# 13.1. Examples of Text and Tasks

**Nguồn web:** [https://learningds.org/ch/13/text_examples.html](https://learningds.org/ch/13/text_examples.html)  
**Nguồn tải:** `web-html` | `ch/13/text_examples`

---

# 13.1. Examples of Text and Tasks#
For each type of task just introduced, we provide a
motivating example. These examples are based on real tasks that we have carried
out, but to focus on the concept, we’ve reduced the data to snippets.
## 13.1.1. Convert Text into a Standard Format#
Let’s say we want to study connections
between population demographics and election results.
To do this, we’ve taken election data from Wikipedia and population data from the US Census Bureau.
The granularity of the data is the county level, and we need to use the county names to join the tables.
Unfortunately, the county names in these two tables don’t always match:
County
State
Voted
0
De Witt County
IL
97.8
1
Lac qui Parle County
MN
98.8
2
Lewis and Clark County
MT
95.2
3
St John the Baptist Parish
LA
52.6
County
State
Population
0
DeWitt
IL
16,798
1
Lac Qui Parle
MN
8,067
2
Lewis & Clark
MT
55,716
3
St. John the Baptist
LA
43,044
We can’t join the tables until we clean the strings to have a common format for county names. We need to change the case of characters, use
common spellings and abbreviations, and address punctuation.
## 13.1.2. Extract a Piece of Text to Create a Feature#
Text data sometimes has a lot of structure, especially when it was generated
by a computer.
As an example, the following is a web server’s log entry.
Notice how the entry has multiple pieces of data, but the pieces don’t have
a consistent delimiter—for instance, the date appears in square brackets,
but other parts of the data appear in quotes and parentheses:
169.237.46.168 - -
[26/Jan/2004:10:47:58 -0800]"GET /stat141/Winter04 HTTP/1.1" 301 328
"http://anson.ucdavis.edu/courses"
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)"
Even though the file format doesn’t align with one of the simple formats we saw
in Chapter 8, we can use text processing techniques to
extract pieces of text to create features.
## 13.1.3. Transform Text into Features#
In Chapter 9, we
created a categorical feature based on the content of the strings. There, we examined the
descriptions of restaurant violations and we created nominal variables for the
presence of particular words.
We’ve displayed a few example violations here:
unclean or degraded floors walls or ceilings
inadequate and inaccessible handwashing facilities
inadequately cleaned or sanitized food contact surfaces
wiping cloths not clean or properly stored or inadequate sanitizer
foods not protected from contamination
unclean nonfood contact surfaces
unclean or unsanitary food contact surfaces
unclean hands or improper use of gloves
inadequate washing facilities or equipment
These new features can be used in an analysis of food safety scores.
Previously, we made simple features that marked whether a description contained
a word like glove or hair. In this chapter, we more formally introduce the regular expression tools that we used to create these features.
## 13.1.4. Text Analysis#
Sometimes we want to compare entire documents.
For example, the US president gives a State of the Union speech every year. Here are the first few lines of the very first speech:
***
State of the Union Address
George Washington
January 8, 1790
Fellow-Citizens of the Senate and House of Representatives:
I embrace with great satisfaction the opportunity which now presents itself
of congratulating you on the present favorable prospects of our public …
We might wonder: How have the State of the Union speeches changed over time? Do different political parties focus on different topics or use different language in their speeches?
To answer these questions, we can transform the speeches into a numeric form
that lets us use statistics to compare them.
These examples serve to illustrate the ideas of string manipulation, regular
expressions, and text analysis. We start with describing simple string manipulation.
