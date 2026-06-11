# 8.5. The Shell and Command-Line Tools

**Nguồn web:** [https://learningds.org/ch/08/files_command_line.html](https://learningds.org/ch/08/files_command_line.html)  
**Nguồn tải:** `web-html` | `ch/08/files_command_line`

---

# 8.5. The Shell and Command-Line Tools#
Nearly all computers provide access to a shell interpreter, such as sh or bash or zsh.  These interpreters typically perform operations on the files on a computer with their own language, syntax, and built-in commands.
We use the term command-line interface (CLI) tools to refer to the commands available in a shell interpreter. Although we only cover a few CLI tools here, there are many useful CLI tools that enable all sorts of operations on files. For instance, the following command in the bash shell
produces a list of all the files in the figures/ folder for this chapter along with their file sizes:
# The dollar sign is the shell prompt, showing the user where to type. It's
# not part of the command itself.
$ ls -l -h figures/
The basic syntax for a shell command is:
command -options arg1 arg2
CLI tools often take one or more arguments, similar to how Python functions
take arguments.
In the shell, we wrap arguments with spaces, not with
parentheses or commas.
The arguments appear at the end of the command line, and they are
usually the name of a file or some text. In the ls example, the
argument to ls is figures/. Additionally, CLI tools support flags that
provide additional options. These flags are specified immediately following the
command name using a dash as a delimiter. In the ls example, we
provided the flags -l (to provide extra information about each file) and -h
(to provide file sizes in a more human-readable format). Many commands have
default arguments and options, and the man tool prints a list of
acceptable options, examples, and defaults for any command.
For example, man ls describes the 30 or so flags available for ls.
Note
All CLI tools we cover in this book are specific to the sh shell
interpreter, the default interpreter for Jupyter installations on macos and
Linux systems at the time of this writing. Windows systems have a different
interpreter, and the commands shown in the book may not run on Windows, although
Windows gives access to an sh interpreter through its Linux Subsystem.
The commands in this section can be run in a terminal application, or through
a terminal opened by Jupyter.
We begin with an exploration of the filesystem containing the content for this chapter, using the ls tool:
$ ls
data                            wrangling_granularity.ipynb
figures                         wrangling_intro.ipynb
wrangling_command_line.ipynb    wrangling_structure.ipynb
wrangling_datasets.ipynb        wrangling_summary.ipynb
wrangling_formats.ipynb
To dive deeper and list the files in the data/ directory, we provide the directory name as an argument to ls:
$ ls -l -L -h data/
total 556664
-rw-r--r--  1 nolan  staff   267M Dec 10 14:03 DAWN-Data.txt
-rw-r--r--  1 nolan  staff   645K Dec 10 14:01 businesses.csv
-rw-r--r--  1 nolan  staff    50K Jan 22 13:09 co2_mm_mlo.txt
-rw-r--r--  1 nolan  staff   455K Dec 10 14:01 inspections.csv
-rw-r--r--  1 nolan  staff   120B Dec 10 14:01 legend.csv
-rw-r--r--  1 nolan  staff   3.6M Dec 10 14:01 violations.csv
We added the -l flag to the command to get more information about each file.
The file size appears in the fifth column of the listing, and it’s more readable as specified by the -h flag.
When we have multiple simple option flags like -l, -h, and -L, we can combine them together as a shorthand:
ls -lLh data/
Note
When working with datasets in this book, our code will often use an additional -L flag for ls and other CLI tools, such as du. We do this because we set up the datasets in the book using shortcuts (called symlinks). Usually, your code won’t need the -L flag unless you’re working with symlinks too.
Other CLI tools for checking file size, are wc and du. The command wc (short for word count) provides helpful information about a file’s size in terms of the number of lines, words, and characters in the file:
$ wc data/DAWN-Data.txt
229211 22695570 280095842 data/DAWN-Data.txt
We can see from the output that DAWN-Data.txt has 229,211 lines and 280,095,842 characters. (The middle value is the file’s word count, which is useful for files that contain sentences and paragraphs bu not very useful for files containing data, such as FWF formatted values.)
The ls tool does not calculate the cumulative size of the contents of a folder. To properly calculate the total size of a folder, including the files in the folder, we use du (short for disk usage). By default, the du tool shows the size in units called blocks:
$ du -L data/
556664	data/
We commonly add the -s flag to du to show the file sizes for both files and folders and the -h flag to display quantities in the standard
KiB, MiB, or GiB format. The asterisk in data/* in the following code tells du to show the size of every item in the_data_ folder:
$ du -Lsh data/*
267M	data/DAWN-Data.txt
648K	data/businesses.csv
52K	data/co2_mm_mlo.txt
456K	data/inspections.csv
4.0K	data/legend.csv
3.6M	data/violations.csv
To check the formatting of a file, we can examine the first few lines with the head command or the last few lines with tail. These CLIs are very useful for peeking at a
file’s contents to determine whether it’s formatted as CSV, TSV, and so on. As an example, let’s
look at the inspections.csv file:
$ head -4 data/inspections.csv
"business_id","score","date","type"
19,"94","20160513","routine"
19,"94","20171211","routine"
24,"98","20171101","routine"
By default, head displays the first 10 lines of a file. If we want to show,
say, four lines, then we add the option -n 4 to our command
(or just -4 for short).
We can print the entire contents of the file using the cat command. However, you
should take care when using this command, as printing a large file can cause a crash.
The legend.csv file is small, and we can use cat to concatenate and print its contents:
$ cat data/legend.csv
"Minimum_Score","Maximum_Score","Description"
0,70,"Poor"
71,85,"Needs Improvement"
86,90,"Adequate"
91,100,"Good"
In many cases, using head or tail alone gives us a good enough sense of the file structure to proceed with loading it into a dataframe.
Finally, the file command can help us determine a file’s encoding:
$ file -I data/*
data/DAWN-Data.txt:   text/plain; charset=us-ascii
data/businesses.csv:  application/csv; charset=iso-8859-1
data/co2_mm_mlo.txt:  text/plain; charset=us-ascii
data/inspections.csv: application/csv; charset=us-ascii
data/legend.csv:      application/csv; charset=us-ascii
data/violations.csv:  application/csv; charset=us-ascii
We see (again) that all of the files are ASCII, except for businesses.csv, which has an
ISO-8859-1 encoding.
Note
Commonly, we open a terminal program to start a shell interpreter. However,
Jupyter notebooks provide a convenience: if a line of code in a Python code
cell is prefixed with the ! character, the line will go directly to the
system’s shell interpreter. For example, running !ls in a Python cell lists
the files in the current directory.
Shell commands give us a programmatic way to work with files, rather than a
point-and-click “manual” approach. They are useful for the following:
Documentation
If you need to record what you did.
Error reduction
If you want to reduce typographical errors and other simple but potentially harmful mistakes.
Reproducibility
If you need to repeat the same process in the future or you
plan to share your process with others. This gives you a record of your actions.
Volume
If you have many repetitive operations to perform, the size of the file you are working with is large, or you need to perform things quickly. CLI tools can help in all these cases.
After the data have been loaded into a dataframe, our next task is to figure
out the table’s shape and granularity. We start by finding the number of rows and columns in the table (its shape). The we need to understand what a row represents before we begin to
check the quality of the data. We cover these topics in the next section.
