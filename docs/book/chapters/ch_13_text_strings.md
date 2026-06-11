# 13.2. String Manipulation

**Nguồn web:** [https://learningds.org/ch/13/text_strings.html](https://learningds.org/ch/13/text_strings.html)  
**Nguồn tải:** `web-html` | `ch/13/text_strings`

---

# 13.2. String Manipulation#
There are a handful of basic string manipulation tools that we use a lot when we work with text:
-
Transform uppercase characters to lowercase (or vice versa).
-
Replace a substring with another or delete the substring.
-
Split a string into pieces at a particular character.
-
Slice a string at specified locations.
We show how we can combine these basic operations to clean up the county names data.
Remember that we have two tables that we want to join, but the county names are
written inconsistently.
Let’s start by converting the county names to a standard format.
## 13.2.1. Converting Text to a Standard Format with Python String Methods#
We need to address the following inconsistencies between the county names in
the two tables:
-
Capitalization: qui versus Qui.
-
Omission of words: County and Parish are absent from the census table.
-
Different abbreviation conventions: & versus and.
-
Different punctuation conventions: St. versus St.
-
Use of whitespace: DeWitt versus De Witt.
When we clean text, it’s often easiest to first convert all of the characters to
lowercase. It’s easier to work entirely with lowercase characters than to try to
track combinations of uppercase and lowercase. Next, we want to fix
inconsistent words by replacing & with and and removing County and
Parish. Finally, we need to fix up punctuation and whitespace inconsistencies.
With just two Python string methods, lower and replace, we can take all of these actions and clean the county names. These are combined into a method called clean_county:
def clean_county(county):
return (county
.lower()
.replace('county', '')
.replace('parish', '')
.replace('&', 'and')
.replace('.', '')
.replace(' ', ''))
Although simple, these methods are the primitives that we can piece together to form more complex string operations. These methods are conveniently defined on all Python strings and do not require importing other modules. Although it is worth familiarizing yourself with the complete list of string
methods, we
describe a few of the most commonly used methods in Table 13.1.
Table 13.1 String methods#
Method
Description
str.lower()
Returns a copy of a string with all letters converted to lowercase
str.replace(a, b)
Replaces all instances of the substring a in str with  substring b
str.strip()
Removes leading and trailing whitespace from str
str.split(a)
Returns substrings of str split at a substring a
str[x:y]
Slices str, returning indices x (inclusive) to y (not inclusive)
We next verify that the clean_county method produces matching county names:
([clean_county(county) for county in election['County']],
[clean_county(county) for county in census['County']])
(['dewitt', 'lacquiparle', 'lewisandclark', 'stjohnthebaptist'],
['dewitt', 'lacquiparle', 'lewisandclark', 'stjohnthebaptist'])
Since the county names now have consistent representations, we can successfully join the two tables.
## 13.2.2. String Methods in pandas#
In the preceding code, we used a loop to transform each county name. The pandas Series
objects provide a convenient way to apply string methods to each item in the
series.
The .str property on pandas Series exposes the same Python string methods. Calling a method on the .str property calls the method on each
item in the series. This allows us to transform each string in the series
without using a loop. We save the transformed counties back into their
originating tables. First we transform the county names in the election table:
election['County'] = (election['County']
.str.lower()
.str.replace('parish', '')
.str.replace('county', '')
.str.replace('&', 'and')
.str.replace('.', '', regex=False)
.str.replace(' ', ''))
census['County'] = (census['County']
.str.lower()
.str.replace('parish', '')
.str.replace('county', '')
.str.replace('&', 'and')
.str.replace('.', '', regex=False)
.str.replace(' ', ''))
We also transform the names in the census table so that the two tables contain the same representations of the county names. We can  join these tables:
election.merge(census, on=['County','State'])
County
State
Voted
Population
0
dewitt
IL
97.8
16,798
1
lacquiparle
MN
98.8
8,067
2
lewisandclark
MT
95.2
55,716
3
stjohnthebaptist
LA
52.6
43,044
Note
Note that we merged on two columns: the county name and the state. We did
this because some states have counties with the same name. For example,
California and New York both have a county called King.
To see the complete list of string methods, we recommend looking at the Python documentation on str
methods and the pandas documentation for the .str
accessor. We did the canonicalization task using only
str.lower() and multiple calls to str.replace(). Next, we extract
text with another string method, str.split().
## 13.2.3. Splitting Strings to Extract Pieces of Text#
Let’s say we want to extract the date from the web server’s log entry:
log_entry
169.237.46.168 - - [26/Jan/2004:10:47:58 -0800]"GET /stat141/Winter04 HTTP/1.1"
301 328 "http://anson.ucdavis.edu/courses""Mozilla/4.0 (compatible; MSIE 6.0;
Windows NT 5.0; .NET CLR 1.1.4322)"
String splitting can help us home in on the pieces of information that form
the date. For example, when we split the string on the left bracket, we get two
strings:
log_entry.split('[')
['169.237.46.168 - - ',
'26/Jan/2004:10:47:58 -0800]"GET /stat141/Winter04 HTTP/1.1" 301 328 "http://anson.ucdavis.edu/courses""Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)"']
The second string has the date information, and to get the day, month, and
year, we can split that string on a colon:
log_entry.split('[')[1].split(':')[0]
'26/Jan/2004'
To separate out the day, month, and year, we can split on the forward slash. Altogether we split the original string three times, each time keeping only the pieces we are interested in:
(log_entry.split('[')[1]
.split(':')[0]
.split('/'))
['26', 'Jan', '2004']
By repeatedly using split(), we can extract many of the parts of the log
entry. But this approach is complicated—if we wanted to
also get the hour, minute, second, and time zone of the activity,
we would need to use split() six times in total.
There’s a simpler way to extract these parts:
import re
pattern = r'[ \[/:\]]'
re.split(pattern, log_entry)[4:11]
['26', 'Jan', '2004', '10', '47', '58', '-0800']
This alternative approach uses a powerful tool called a regular expression,
which we cover in the next section.
