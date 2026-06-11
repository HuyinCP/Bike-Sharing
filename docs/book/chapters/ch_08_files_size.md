# 8.4. File Size

**Nguồn web:** [https://learningds.org/ch/08/files_size.html](https://learningds.org/ch/08/files_size.html)  
**Nguồn tải:** `web-html` | `ch/08/files_size`

---

# 8.4. File Size#
Computers have finite resources. You have likely
encountered these limits firsthand if your computer has slowed down from having
too many applications open at once. We want to make sure that we do not
exceed the computer’s limits while working with data, and we might choose to examine a file differently depending on its size. If we know that our dataset is relatively small, then a text editor or a spreadsheet can be convenient for looking at the data. On the other hand, for large datasets, a more programmatic exploration or even distributed computing tools may be needed.
In many situations, we analyze datasets downloaded from the internet. These
files reside on the computer’s disk storage. In order to use Python to
explore and manipulate the data, we need to read the data into the computer’s
memory, also known as random access memory (RAM). All Python code requires
the use of RAM, no matter how short the code is.
A computer’s RAM is typically much smaller than its disk storage. For
example, one computer model released in 2018 had 32 times more disk storage
than RAM.  Unfortunately, this means that data files can often be much bigger
than what is feasible to read into memory.
Both disk storage and RAM capacity are measured in terms of bytes (eight 0s and 1s). Roughly
speaking, each character in a text file adds one byte to a file’s size.
To succinctly describe the sizes of larger files, we use the prefixes described
in Table 8.1. For example, a file containing 52,428,800 characters takes
up \(5,242,8800 / 1,024^2 = 50~{\textrm{mebibytes}}\), or 50 MiB on disk.
Table 8.1 Prefixes for common file sizes.#
Multiple
Notation
Number of bytes
Kibibyte
KiB
1,024
Mebibyte
MiB
1,024²
Gibibyte
GiB
1,024³
Tebibyte
TiB
1,024⁴
Pebibyte
PiB
1,024⁵
Note
Why use multiples of 1,024 instead of simple multiples of 1,000 for these
prefixes? This is a historical result of the fact that most computers
use a binary number scheme where powers of 2 are simpler to represent (\(1,024 = 2^{10}\)). You also see the typical SI prefixes used to describe size—kilobytes, megabytes,
and gigabytes, for example. Unfortunately, these prefixes are used
inconsistently. Sometimes a kilobyte refers to 1,000 bytes; other times, a
kilobyte refers to 1,024 bytes. To avoid confusion, we stick to kibi-,
mebi-, and gibibytes, which clearly represent multiples of 1,024.
It is not uncommon to have a data file happily stored on a computer that will overflow the computer’s memory if we attempt to
manipulate it with a program. So we often begin our
data work by making sure the files are of manageable size. To do this, we use the built-in os library:
from pathlib import Path
import os
kib = 1024
line = '{:<25} {}'.format
print(line('File', 'Size (KiB)'))
for filepath in Path('data').glob('*'):
size = os.path.getsize(filepath)
print(line(str(filepath), np.round(size / kib)))
File                      Size (KiB)
data/inspections.csv      455.0
data/co2_mm_mlo.txt       50.0
data/violations.csv       3639.0
data/DAWN-Data.txt        273531.0
data/legend.csv           0.0
data/businesses.csv       645.0
We see that the businesses.csv file takes up 645 KiB on disk, making it well
within the memory capacities of most systems. Although the violations.csv
file takes up 3.6 MiB of disk storage, most machines can easily read it into a
pandas DataFrame too. But DAWN-Data.txt, which contains the DAWN survey data,
is much larger.
The DAWN file takes up roughly 270 MiB of disk storage, and while some computers
can work with this file in memory, it can slow down other systems. To make
this data more manageable in Python, we can, for example, load in a subset of the columns
rather than all of them.
Sometimes we are interested in the total size of a folder
instead of the size of individual files. For example, we have three restaurant files,
and we might like to see whether we can combine all the data into a single dataframe. In the following code, we calculate the size of the data folder, including all files in it:
mib = 1024**2
total = 0
for filepath in Path('data').glob('*'):
total += os.path.getsize(filepath) / mib
print(f'The data/ folder contains {total:.2f} MiB')
The data/ folder contains 271.80 MiB
Note
As a rule of thumb, reading in a file using pandas
usually requires at least five times
the available memory as the file size.
For example, reading in a 1 GiB file typically requires at least 5 GiB of available memory.
Memory is shared by all programs running on a computer, including the
operating system, web browsers, and Jupyter notebook itself. A computer
with 4 GiB total RAM might have only 1 GiB available RAM with many applications
running. With 1 GiB available RAM, it is unlikely that pandas will be able to
read in a 1 GiB file.
There are several strategies for working with data that are far larger than what is feasible to load into memory. We describe a few of them next.
The popular term big data generally refers to the scenario where the data are large enough that even top-of-the-line computers can’t read the data directly into memory.
This is a common scenario in scientific domains like astronomy, where telescopes capture images of space that can be petabytes (\( 2^{50} \)) in size. While not quite as big, social media giants, health-care providers, and other companies can also struggle with large amounts of data.
Figuring out how to draw insights from these datasets is an important research
problem that motivates the fields of database engineering and distributed
computing. While we won’t cover these fields in this book, we provide a brief overview of basic approaches:
Subset the data
One simple approach is to work with portions of data. Rather than
loading in the entire source file, we can either select a specific part of it
(e.g., one day’s worth of data) or randomly sample the dataset. Because
of its simplicity, we use this approach quite often in this book. The natural
downside is that we lose many of the benefits of analyzing a large
dataset, like being able to study rare events.
Use a database system.
As discussed in Chapter 7,
relational database management systems (RDBMSs) are specifically designed to
store large datasets. SQLite is a useful system for working with datasets that
are too large to fit in memory but small enough to fit on disk for a single
machine. For datasets that are too large to fit on a single machine, more
scalable database systems like MySQL and PostgreSQL can be used. These systems
can manipulate data that are too big to fit into memory by using SQL queries.
Because of their advantages, RDBMSs are commonly used for data storage in
research and industry settings. One downside is that they often require a
separate server for the data that needs its own configuration. Another downside
is that SQL is less flexible in what it can compute than Python, which becomes
especially relevant for modeling. A useful hybrid approach is to use SQL to
subset, aggregate, or sample the data into batches that are small enough to
read into Python. Then we can use Python for more sophisticated analyses.
Use a distributed computing system
Another approach to handle complex
computations on large datasets is to use a distributed computing system like
MapReduce, Spark, or Ray.
These systems work best on tasks that can be split into many smaller parts
where they divide datasets into smaller pieces and run programs on
all of the smaller datasets at once.
These systems have great flexibility and can be used
in a variety of scenarios. Their main downside is
that they can require a lot of work to install and configure properly
because they are typically installed across many computers that need to
coordinate with one another.
It can be convenient to use Python to determine a file format, encoding, and size.
Another powerful tool for working with files is the shell; the shell is widely
used and has a more succinct syntax than Python.
In the next section, we introduce a few command-line tools available in the shell for carrying out the same tasks of finding out information about a file before reading it into a data
