# 8.3. File Encoding

**Nguồn web:** [https://learningds.org/ch/08/files_encoding.html](https://learningds.org/ch/08/files_encoding.html)  
**Nguồn tải:** `web-html` | `ch/08/files_encoding`

---

# 8.3. File Encoding#
Computers store data as sequences of bits: 0s and 1s.
Character encodings, like ASCII, tell the computer how to translate between bits and text.
For example, in ASCII, the bits 100 001 stand for the letter A and 100 010 for B.
The most basic kind of plain text supports only standard ASCII characters, which
includes the uppercase and lowercase English letters, numbers, punctuation symbols, and spaces.
ASCII encoding does not include a lot of special characters or characters from other languages.
Other, more modern character encodings have many more characters that can be represented.
Common encodings for documents and web pages are Latin-1 (ISO-8859-1) and UTF-8. UTF-8 has over a
million characters and is backward compatible with ASCII, meaning that it
uses the same representation for English letters, numbers, and punctuation as
ASCII.
When we have a text file, we usually need to figure out its
encoding. If we choose the wrong encoding to read in a file, Python
either reads incorrect values or throws an error. The best way to find the encoding
is by checking the data’s documentation, which often explicitly says what the
encoding is.
When we don’t know the encoding, we have to make a guess. The chardet
package has a function called detect() that infers a file’s encoding.
Since these guesses are imperfect, the function also returns a confidence
between 0 and 1. We use this function to look at the files from our examples:
import chardet
line = '{:<25} {:<10} {}'.format
# for each file, print its name, encoding & confidence in the encoding
print(line('File Name', 'Encoding', 'Confidence'))
for filepath in Path('data').glob('*'):
result = chardet.detect(filepath.read_bytes())
print(line(str(filepath), result['encoding'], result['confidence']))
File Name                 Encoding   Confidence
data/inspections.csv      ascii      1.0
data/co2_mm_mlo.txt       ascii      1.0
data/violations.csv       ascii      1.0
data/DAWN-Data.txt        ascii      1.0
data/legend.csv           ascii      1.0
data/businesses.csv       ISO-8859-1 0.73
The detection function is quite certain that all but one of the files are
ASCII encoded. The exception is businesses.csv, which appears to have an ISO-8859-1
encoding. We run into trouble if we ignore this encoding and try to read the
business file into pandas without specifying the special encoding:
# naively reads file without considering encoding
>>> pd.read_csv('data/businesses.csv')
[...stack trace omitted...]
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd1 in
position 8: invalid continuation byte
To successfully read the data, we must specify the ISO-8859-1 encoding:
bus = pd.read_csv('data/businesses.csv', encoding='ISO-8859-1')
business_id
name
address
postal_code
0
19
NRGIZE LIFESTYLE CAFE
1200 VAN NESS AVE, 3RD FLOOR
94109
1
24
OMNI S.F. HOTEL - 2ND FLOOR PANTRY
500 CALIFORNIA ST, 2ND  FLOOR
94104
2
31
NORMAN'S ICE CREAM AND FREEZES
2801 LEAVENWORTH ST
94133
3
45
CHARLIE'S DELI CAFE
3202 FOLSOM ST
94110
File encoding can be a bit mysterious to figure out, and unless there is metadata that explicitly gives us the encoding, guesswork comes into play.
When an encoding is not 100% confirmed, it’s a good idea to seek additional documentation.
Another potentially important aspect of a source file is its size.
If a file is huge, then we might not be able to read it into a dataframe.
In the next section, we discuss how to figure out a source file’s size.
