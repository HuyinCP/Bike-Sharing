# 8.2. File Formats

**Nguồn web:** [https://learningds.org/ch/08/files_formats.html](https://learningds.org/ch/08/files_formats.html)  
**Nguồn tải:** `web-html` | `ch/08/files_formats`

---

# 8.2. File Formats#
A file format describes how data are stored on a computer’s disk or other storage device.
Understanding the file format helps us figure out how to read the data into Python in order to work with it
as a data table.
In this section, we introduce several popular formats used to store data tables.
These are all plain-text formats, meaning they are easy for us to read with a text editor like VS Code, Sublime, Vim, or Emacs.
Note
The file format and the structure of the data are two
different things.
We consider the data structure to be a mental representation of the data that tells us what kinds of operations we can do.
For example, a table structure corresponds to data values arranged in rows
and columns.
But the same table can be stored in many different types of file formats.
The first format we describe is the delimited file format.
## 8.2.1. Delimited Format#
Delimited formats use a specific character to separate data values.
Usually, these separators are either a comma (comma-separated-values, or CSV
for short), a tab (tab-separated values or TSV), whitespace, or a colon. These
formats are natural for storing data that have a table structure.
Each line in the file represents a record, which is delimited by newline (\n or \r\n) characters.
And within a line, the record’s
information is delimited by the comma character (,) for CSV or the tab
character (\t) for TSV, and so on. The first line of these files often contains the names of the table’s columns/features.
The San Francisco restaurant scores are stored in CSV-formatted files.
Let’s display the first few lines of the inspections.csv file. In Python, the built-in pathlib library has a useful Path object to specify paths to files and folders that work across platforms.
This file is within the data folder, so we use Path() to create the full pathname:
from pathlib import Path
# Create a Path pointing to our data file
insp_path = Path() / 'data' / 'inspections.csv'
Note
Paths are tricky when working across different
operating systems (OSs). For instance, a typical path in Windows might look like
C:\files\data.csv, while a path in Unix or macos might look like
~/files/data.csv. Because of this, code that works on one OS can fail to run
on other OSs.
The pathlib Python library was created to avoid OS-specific path issues. By
using it, the code shown here is more portable—it works across Windows,
macos, and Unix.
The Path object in the following code has many useful methods, such as read_text(), which reads in the entire contents of the file as a string:
text = insp_path.read_text()
# Print first five lines
print('\n'.join(text.split('\n')[:5]))
"business_id","score","date","type"
19,"94","20160513","routine"
19,"94","20171211","routine"
24,"98","20171101","routine"
24,"98","20161005","routine"
Notice that the field names appear in the first line of the file; these names are comma separated and in
quotes. We see four fields: the business identifier, the
restaurant’s score, the date of the inspection, and the type of inspection.
Each line in the file corresponds to one inspection, and the ID, score, date,
and type values are separated by commas. In addition to identifying the file
format, we also want to identify the format of the features. We see two things
of note: the scores and dates both appear as strings. We will want to convert
the scores to numbers so that we can calculate summary statistics and create visualizations.
And we will convert the date into a date-time format so
that we can make time-series plots. We show how to carry out these
transformations in Chapter 9.
Displaying the first few lines of a file is something we’ll do often, so we create a function as a shortcut:
def head(filepath, n=5, width=-1):
'''Prints the width characters of first n lines of filepath'''
with filepath.open() as f:
for _ in range(n):
(print(f.readline(), end='') if width < 0
else print(f.readline()[:width]))
Note
People often confuse CSV and TSV files with spreadsheets. This is in part
because most spreadsheet software (like Microsoft Excel) will automatically
display a CSV file as a table in a workbook. Behind the scenes, Excel looks at
the file format and encoding just like we’ve done in this section. However,
Excel files have a different format than CSV and TSV files, and we need to use
different pandas functions to read these formats into Python.
All three of the restaurant source files are CSV formatted. In contrast, the DAWN source file has a fixed-width format. We describe this kind of formatting next.
## 8.2.2. Fixed-Width Format#
The fixed-width format (FWF) does not use delimiters to separate data
values. Instead, the values for a specific field appear in the exact same
position in each line. The DAWN source file has this format.
Each line in the file is very long. For display purposes,
we only show the first few characters from the first five lines in the file:
dawn_path = Path() / 'data' / 'DAWN-Data.txt'
head(dawn_path, width=65)
1 2251082    .9426354082   3 4 1 2201141 2 865 105 1102005 1
2 2291292   5.9920106887   911 1 3201134 12077  81  82 283-8
3 7 7 251   4.7231718669   611 2 2201143 12313   1  12  -7-8
410 8 292   4.0801470012   6 2 1 3201122 1 234 358  99 215 2
5 122 942   5.1777093467  10 6 1 3201134 3 865 105 1102005 1
Notice how the values appear to align from one row to the next.
For example, there is a decimal point in the same position (the 19th character) in each line.
Notice also that some of the values seem to be squished together, and
we need to know the exact position of each piece of information in
a line in order to make sense of it. SAMHSA provides a 2,000-page codebook with
all of this information, including some basic checks, so that we can confirm that we have correctly
read the file. For instance, the codebook tells us that the age field appears in positions 34–35 and is coded in intervals from
1 to 11. The first two records shown in the preceding code have age categories of 4 and 11;
the codebook tells us that a 4 stands for the age bracket “6 to 11” and 11 is for “65+.”
Note
A widely adopted convention is to use the filename extension, such as
.csv, .tsv, and .txt, to indicate the format of the contents of the file.
Filenames that end with .csv are expected to contain comma-separated values, and those ending with
.tsv are expected to contain tab-separated values; .txt generally denotes plain text without a designated format.
However, these extension names are only suggestions. Even if a file has a .csv extension,
the actual contents might not be formatted properly! It’s a good practice to
inspect the contents of the file before loading it into a dataframe. If the
file is not too large, you can open and examine it with a plain-text editor.
Otherwise, you can view a couple of lines using .readline() or shell
command.
Other plain-ext formats that are popular include hierarchical formats and loosely formatted text (in contrast to formats that directly support table structures). These are covered in greater detail in other chapters, but for completeness, we briefly describe them here.
## 8.2.3. Hierarchical Formats#
Hierarchical formats store data in a nested form. For instance,
JavaScript Object Notation (JSON), which is commonly used for communication by web servers, includes key-value pairs and arrays that can be nested, similar to a Python dictionary. The XML and HTML are other common formats for storing documents on the internet. Like JSON, these files also have a hierarchical, key-value format. We cover both formats (JSON and XML) in more detail in Chapter 14.
Next, we briefly describe other plain-text files that don’t fall into any of the previous categories but still have some structure to them that enables us to read and extract information.
## 8.2.4. Loosely Formatted Text#
Web logs, instrument readings, and program logs typically provide data in plain text.  For example, here is one line of a web log (we’ve split it across multiple lines for readability). It contains information such as the date, time, and type of request made to a website:
169.237.46.168 - -
[26/Jan/2004:10:47:58 -0800]"GET /stat141/Winter04 HTTP/1.1" 301 328
"http://anson.ucdavis.edu/courses"
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)"
There are organizational patterns present, but not in a simple delimited format. This is what we mean by “loosely formatted.” We see that the date and time appear between square brackets, and the type of request (GET in this case) follows the date-time information and appears in quotes. In Chapter 13, we use these observations about the web log’s format and string manipulation tools to extract values of interest into a data table.
As another example, here is a single record taken from a wireless device log. The device reports the timestamp, the identifier, its location, and the signal strengths that it picks up from other devices. This information uses a combination of formats: key-value pairs, semicolon-delimited values, and comma-delimited values:
t=1139644637174;id=00:02:2D:21:0F:33;pos=2.0,0.0,0.0;degree=45.5;
00:14:bf:b1:97:8a=-33,2437000000,3;00:14:bf:b1:97:8a=-38,2437000000,3;
Like with the web logs, we can use string manipulation and the patterns in the records to extract features into a table.
We have primarily introduced formats for plain-text data that are widely used for storing and exchanging tables. The CSV format is the most common, but others, such as tab-separated and fixed-width formats, are also prevalent. And, there are many types of file formats that store data!
So far, we have used the term plain text to broadly cover formats that can be viewed with a text editor. However, a plain-text file may have different encodings, and if we don’t specify the encoding correctly, the values in the dataframe might contain gibberish. We give an overview of file encoding next.
