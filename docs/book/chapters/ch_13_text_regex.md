# 13.3. Regular Expressions

**Nguồn web:** [https://learningds.org/ch/13/text_regex.html](https://learningds.org/ch/13/text_regex.html)  
**Nguồn tải:** `web-html` | `ch/13/text_regex`

---

# 13.3. Regular Expressions#
Regular expressions (or regex for short) are special patterns that we use
to match parts of strings.
Think about the format of a Social Security number (SSN) like 134-42-2012.
To describe this format, we
might say that SSNs consist of three digits, then a dash, two digits, another
dash, then four digits. Regexes let us capture this pattern in code.
Regexes give us a compact and powerful way to describe this pattern of digits and dashes. The syntax of regular expressions is fortunately quite
simple to learn; we introduce nearly all of the syntax in this section alone.
As we introduce the concepts, we tackle some of the examples described in an
earlier section and show how to carry out the tasks with regular expressions.
Almost all programming languages have a library to match patterns using regular
expressions, making regular expressions useful in any programming language. We use some of the common methods available in the Python
built-in re module to accomplish the tasks from the examples. These methods
are summarized in Table 13.7 at the end of this section, where the basic usage and
return value are briefly described. Since we only cover a few of the most
commonly used methods, you may find it useful to consult the official
documentation on the re module as well.
Regular expressions are based on searching a string one character (aka
literal) at a time for a pattern. We call this notion concatenation of
literals.
## 13.3.1. Concatenation of Literals#
Concatenation is best explained with a basic example. Suppose we are looking
for the pattern cat in the string cards scatter!. Here’s how the computer matches a literal pattern like cat:
-
Begin with the first character in the string (c).
-
Does the character in the string match the first character in the pattern (c)?
-
No: move on to the next character of the string. Return to step 2.
-
Yes: does the rest of the pattern match (a, then t)?
-
No: move on to the next character of the string (one character past the location in step 2). Return to step 2.
-
Yes: report that the pattern was found.
Figure 13.1 contains a diagram of
the idea behind this search through the string
one character at a time. The pattern “cat” is found within the string
cards scatter! in positions 8–10. Once you get the hang of this process, you can
move on to the richer set of patterns; they all follow this basic
paradigm.
Fig. 13.1 To match literal patterns, the regex engine moves along the string and checks one literal at a time for a match of the entire pattern. Notice that the pattern is found within the word scatters and that a partial match is found in cards.#
Note
In the preceding example, we observe that regular expressions can match patterns
that appear anywhere in the input string. In Python, this behavior differs
depending on the method used to match the regex—some methods only return a
match if the regex appears at the start of the string; other methods return a
match anywhere in the string.
These richer patterns are made of character classes and metacharacters like wildcards. We describe them in the subsections that follow.
### 13.3.1.1. Character classes#
We can make patterns more flexible by using a character class
(also known as a character set), which
lets us specify a collection of equivalent characters to match. This allows us
to create more relaxed matches. To create a character class, wrap the set of
desired characters in brackets [ ].
For example, the pattern [0123456789] means “match any literal
within the brackets”—in this case, any single digit.
Then, the following regular expression matches three digits:
[0123456789][0123456789][0123456789]
This is such a commonly used character class that
there is a shorthand notation for the range of digits, [0-9]. Character
classes allow us to create a regex for SSNs:
[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]
Two other ranges that are commonly used in character classes are [a-z] for
lowercase and [A-Z] for uppercase letters. We can combine ranges with other
equivalent characters and use partial ranges. For example, [a-cX-Z27] is
equivalent to the character class [abcXYZ27].
Let’s return to our original pattern cat and modify it to include two character classes:
c[oa][td]
This pattern matches cat, but it also matches cot, cad, and cod:
Regex: c[oa][td]
Text: The cat eats cod, cads, and cots, but not coats.
Matches:     ***      ***  ***       ***
The idea of moving through the string one character at a time still remains the core notion, but now there’s a bit more flexibility in which literal is considered a match.
### 13.3.1.2. Wildcard character#
When we really don’t care what the literal is, we can specify this with ., the
period character. This matches any character except a newline.
### 13.3.1.3. Negated character classes#
A negated character class matches any character
except those between the square brackets. To create a negated character
class, place the caret symbol as the first character after the left square
bracket. For example, [^0-9] matches any character except a digit.
### 13.3.1.4. Shorthands for character classes#
Some character sets are so common that there are shorthands for them. For example, \d is short for [0-9]. We can use this shorthand to simplify our search for SSN:
\d\d\d-\d\d-\d\d\d\d
Our regular expression for SSNs isn’t quite bulletproof. If the string has extra digits at the beginning or end of the pattern we’re looking for, then we still get a match. Note that we add the r character before the quotes to create a raw string, which makes regexes easier to write:
Regex: \d\d\d-\d\d-\d\d\d\d
Text: My other number is 6382-13-38420.
Matches:                     ***********
We can remedy the situation with a different sort of metacharacter: one that matches a word boundary.
### 13.3.1.5. Anchors and boundaries#
At times we want to match a position before, after, or between characters. One example is to locate the beginning or end of a string; these are called anchors. Another is to locate the beginning or end of a word, which we call a boundary. The metacharacter \b denotes the boundary of a word. It has 0 length, and it matches whitespace or punctuation on the boundary of the pattern. We can use it to fix our regular expression for SSNs:
Regex: \d\d\d-\d\d-\d\d\d\
Text: My other number is 6382-13-38420.
Matches:
Regex: \b\d\d\d-\d\d-\d\d\d\d\b
Text: My reeeal number is 382-13-3842.
Matches:                     ***********
### 13.3.1.6. Escaping metacharacters#
We have now seen several special characters, called metacharacters: [ and
] denotes a character class, ^ switches to a negated character class, .
represents any character, and - denotes a range. But sometimes we might want
to create a pattern that matches one of these literals. When this happens, we
must escape it with a backslash. For example, we can match the literal left
bracket character using the regex \[:
Regex: \[
Text: Today is [2022/01/01]
Matches:          *
Next, we show how quantifiers can help create a more compact and clear
regular expression for SSNs.
## 13.3.2. Quantifiers#
To create a regex to match SSNs, we wrote:
\b[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]\b
This matches a “word” consisting of three digits, a dash, two more digits, a dash, and four more digits.
Quantifiers allow us to match multiple consecutive appearances of a literal. We
specify the number of repetitions by placing the number in curly braces { }.
Let’s use Python’s built-in re module for matching this pattern:
import re
ssn_re = r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'
re.findall(ssn_re, 'My SSN is 382-34-3840.')
['382-34-3840']
Our pattern shouldn’t match phone numbers. Let’s try it:
re.findall(ssn_re, 'My phone is 382-123-3842.')
[]
A quantifier always modifies the character or character class to its immediate
left. Table 13.2 shows the complete syntax for quantifiers.
Table 13.2 Quantifier examples#
Quantifier
Meaning
{m, n}
Match the preceding character m to n times.
{m}
Match the preceding character exactly m times.
{m,}
Match the preceding character at least m times.
{,n}
Match the preceding character at most n times.
Some commonly used quantifiers have a shorthand, as shown in Table 13.3.
Table 13.3 Shorthand quantifiers#
Symbol
Quantifier
Meaning
*
{0,}
Match the preceding character 0 or more times.
+
{1,}
Match the preceding character 1 or more times.
?
{0,1}
Match the preceding character 0 or 1 time.
Quantifiers are greedy and will return the longest match possible. This sometimes results in
surprising behavior. Since an SSN starts and ends with a digit, we might think
the following shorter regex will be a simpler approach for finding SSNs.  Can
you figure out what went wrong in the matching?
ssn_re_dot = r'[0-9].+[0-9]'
re.findall(ssn_re_dot, 'My SSN is 382-34-3842 and hers is 382-34-3333.')
['382-34-3842 and hers is 382-34-3333']
Notice that we use the metacharacter . to match any character. In many cases, using a more specific character class prevents these false “over-matches.” Our earlier pattern that includes word boundaries does this:
re.findall(ssn_re, 'My SSN is 382-34-3842 and hers is 382-34-3333.')
['382-34-3842', '382-34-3333']
Some platforms allow you to turn off greedy matching and use lazy matching, which returns the shortest string.
Literal concatenation and quantifiers are two of the core concepts in regular
expressions. Next, we introduce two more core concepts: alternation and grouping.
## 13.3.3. Alternation and Grouping to Create Features#
Character classes let us match multiple options for a single literal.
We can use alternation to match multiple options for a group of literals.
For instance, in the food safety example in
Chapter 9, we marked violations related to
body parts by seeing if the violation had the substring
hand, nail, hair, or glove.
We can use the | character in a regex to specify this alteration:
body_re = r"hand|nail|hair|glove"
re.findall(body_re, "unclean hands or improper use of gloves")
['hand', 'glove']
re.findall(body_re, "Unsanitary employee garments hair or nails")
['hair', 'nail']
With parentheses we can locate parts of a pattern, which are called regex groups. For example, we can use regex groups to extract the day, month, year, and time from the web server log entry:
# This pattern matches the entire timestamp
time_re = r"\[[0-9]{2}/[a-zA-z]{3}/[0-9]{4}:[0-9:\- ]*\]"
re.findall(time_re, log_entry)
['[26/Jan/2004:10:47:58 -0800]']
# Same regex, but we use parens to make regex groups...
time_re = r"\[([0-9]{2})/([a-zA-z]{3})/([0-9]{4}):([0-9:\- ]*)\]"
# ...which tells findall() to split up the match into its groups
re.findall(time_re, log_entry)
[('26', 'Jan', '2004', '10:47:58 -0800')]
As we can see, re.findall returns a list of tuples containing the individual
components of the date and time of the web log.
We have introduced a lot of terminology, so
in the next section we bring it all together into a set of tables for easy reference.
## 13.3.4. Reference Tables#
We conclude this section with a few tables that summarize order of
operation, metacharacters, and shorthands for character classes.
We also provide tables summarizing the handful of methods in the re
Python library that we have used in this section.
The four basic operations for regular expressions—concatenation, quantifying,
alternation, and grouping—have an order of precedence, which we make explicit
in Table 13.4.
Table 13.4 Order of operations#
Operation
Order
Example
Matches
Concatenation
3
cat
cat
Alternation
4
cat|mouse
cat and mouse
Quantifying
2
cat?
ca and cat
Grouping
1
c(at)?
c and cat
Table 13.5 provides a list of the metacharacters introduced in this
section, plus a few more. The column labeled “Doesn’t match” gives examples of
strings that the example regexes don’t match.
Table 13.5 Metacharacters#
Char
Description
Example
Matches
Doesn’t match
.
Any character except \n
...
abc
ab
[ ]
Any character inside brackets
[cb.]ar
car
.ar
jar
[^ ]
Any character not inside brackets
[^b]ar
car
par
bar
ar
*
≥ 0 or more of previous symbol, shorthand for {0,}
[pb]*ark
bbark
ark
dark
+
≥ 1 or more of previous symbol, shorthand for {1,}
[pb]+ark
bbpark
bark
dark
ark
?
0 or 1 of previous symbol, shorthand for {0,1}
s?he
she
he
the
{n}
Exactly n of previous symbol
hello{3}
hellooo
hello
|
Pattern before or after bar
we|[ui]s
we
us
is
es
e
s
\
Escape next character
\[hi\]
[hi]
hi
^
Beginning of line
^ark
ark two
dark
$
End of line
ark$
noahs ark
noahs arks
\b
Word boundary
ark\b
ark of noah
noahs arks
Additionally, in Table 13.6, we provide shorthands for some commonly used character
sets. These shorthands don’t need [ ].
Table 13.6 Character class shorthands #
Description
Bracket form
Shorthand
Alphanumeric character
[a-zA-Z0-9_]
\w
Not an alphanumeric character
[^a-zA-Z0-9_]
\W
Digit
[0-9]
\d
Not a digit
[^0-9]
\D
Whitespace
[\t\n\f\r\p{Z}]
\s
Not whitespace
[^\t\n\f\r\p{z}]
\S
We used the following methods in re in this chapter. The names of the methods
are indicative of the functionality they perform: search or
match a pattern in a
string; find all cases of a pattern in a string; substitute all occurrences
of a pattern with a substring; and split a string into pieces at the pattern.
Each requires a pattern and string to be specified, and some have
extra arguments.
Table 13.7 provides the format of the method usage and a
description of the return value.
Table 13.7 Regular expression methods#
Method
Return value
re.search(pattern, string)
Truthy match object if the pattern is found anywhere in the string, otherwise None
re.match(pattern, string)
Truthy match object if the pattern is found at the beginning of the string, otherwise None
re.findall(pattern, string)
List of all matches of pattern in string
re.sub(pattern, replacement, string)
String where all occurrences of pattern are replaced by  replacement in the string
re.split(pattern, string)
List of the pieces of string around the occurrences of pattern
As we saw in the previous section, pandas Series objects have a .str property
that supports string manipulation using Python string methods. Conveniently,
the .str property also supports some functions from the re module. Table 13.8 shows the analogous functionality from Table 13.7 of the re
methods. Each requires a pattern.
See the pandas docs for a complete list of
string methods.
Table 13.8 Regular expressions in pandas#
Method
Return value
str.contains(pattern, regex=True)
Series of booleans indicating whether the pattern is found
str.findall(pattern, regex=True)
List of all matches of pattern
str.replace(pattern, replacement, regex=True)
Series with all matching occurrences of pattern replaced by replacement
str.split(pattern, regex=True)
Series of lists of strings around given pattern
Regular expressions are a powerful tool, but they’re somewhat notorious for being difficult to read and debug. We close with some advice for using regexes:
-
Develop your regular expression on simple test strings to see what the pattern matches.
-
If a pattern matches nothing, try weakening it by dropping part of the pattern. Then tighten it incrementally to see how the matching evolves. (Online regex checking tools can be very helpful here.)
-
Make the pattern only as specific as it needs to be for the data at hand.
-
Use raw strings whenever possible for cleaner patterns, especially when a pattern includes a backslash.
-
When you have lots of long strings, consider using compiled patterns because they can be faster to match (see compile() in the re library).
In the next section, we carry out an example text analysis.
We clean the data
using regular expressions and string manipulation, convert the text into
quantitative data, and analyze the text via these derived quantities.
