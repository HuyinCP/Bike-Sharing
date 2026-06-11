# 21.2. Obtaining and Wrangling the Data

**Nguồn web:** [https://learningds.org/ch/21/fake_news_data.html](https://learningds.org/ch/21/fake_news_data.html)  
**Nguồn tải:** `web-html` | `ch/21/fake_news_data`

---

# 21.2. Obtaining and Wrangling the Data#
Let’s get the data into Python using the GitHub page for FakeNewsNet. Reading over the repository description and code, we find that the repository doesn’t actually store the news articles itself. Instead, running the repository code will scrape news articles from online web pages directly (using techniques we covered in Chapter 14). This presents a challenge: if an article is no longer available online, it likely will be missing from our dataset. Noting this, let’s proceed with downloading the data.
Note
The FakeNewsNet code highlights one challenge in reproducible research—online datasets change over time, but it can be difficult (or even illegal) to store and share copies of this data. For example, other parts of the FakeNewsNet dataset use Twitter posts, but the dataset creators would violate Twitter’s terms and services if they stored copies of the posts in their repository. When working with data gathered from the web, we suggest documenting the date the data were gathered and reading the terms and services of the data sources carefully.
Running the script to download the Politifact data takes about an hour.
After that, we place the datafiles into the data/politifact folder.
The articles that Politifact labeled as fake and real
are in data/politifact/fake and data/politifact/real.
Let’s take a look at one of the articles labeled “real”:
!ls -l data/politifact/real | head -n 5
total 0
drwxr-xr-x  2 sam  staff  64 Jul 14  2022 politifact100
drwxr-xr-x  3 sam  staff  96 Jul 14  2022 politifact1013
drwxr-xr-x  3 sam  staff  96 Jul 14  2022 politifact1014
drwxr-xr-x  2 sam  staff  64 Jul 14  2022 politifact10185
ls: stdout: Undefined error: 0
!ls -lh data/politifact/real/politifact1013/
total 16
-rw-r--r--  1 sam  staff   5.7K Jul 14  2022 news content.json
Each article’s data is stored in a JSON file named news content.json.
Let’s load the JSON for one article into a Python dictionary (see Chapter 14):
import json
from pathlib import Path
article_path = Path('data/politifact/real/politifact1013/news content.json')
article_json = json.loads(article_path.read_text())
Here, we’ve displayed the keys and values in article_json as a table:
display_df(
pd.DataFrame(article_json.items(), columns=['key', 'value']).set_index('key'),
rows=13)
value
key
url
http://www.senate.gov/legislative/LIS/roll_cal...
text
Roll Call Vote 111th Congress - 1st Session\n\...
images
[http://statse.webtrendslive.com/dcs222dj3ow9j...
top_img
http://www.senate.gov/resources/images/us_sen.ico
keywords
[]
authors
[]
canonical_link
title
U.S. Senate: U.S. Senate Roll Call Votes 111th...
meta_data
{'viewport': 'width=device-width, initial-scal...
movies
[]
publish_date
None
source
http://www.senate.gov
summary
There are many fields in the JSON file, but for this analysis we only look at a
few that are primarily related to the content of the article: the article’s title, text content, URL, and publication date.
We create a data frame where each row represents one article (the granularity in a news story).
To do this, we load in each available JSON file as a Python dictionary, and then
extract the fields of interest to store as a pandas DataFrame named df_raw:
from pathlib import Path
def df_row(content_json):
return {
'url': content_json['url'],
'text': content_json['text'],
'title': content_json['title'],
'publish_date': content_json['publish_date'],
}
def load_json(folder, label):
filepath = folder / 'news content.json'
data = df_row(json.loads(filepath.read_text())) if filepath.exists() else {}
return {
**data,
'label': label,
}
fakes = Path('data/politifact/fake')
reals = Path('data/politifact/real')
df_raw = pd.DataFrame([load_json(path, 'fake') for path in fakes.iterdir()] +
[load_json(path, 'real') for path in reals.iterdir()])
df_raw.head(2)
url
text
title
publish_date
label
0
dailybuzzlive.com/cannibals-arrested-florida/
Police in Vernal Heights, Florida, arrested 3-...
Cannibals Arrested in Florida Claim Eating Hum...
1.62e+09
fake
1
https://web.archive.org/web/20171228192703/htt...
WASHINGTON — Rod Jay Rosenstein, Deputy Attorn...
BREAKING: Trump fires Deputy Attorney General ...
1.45e+09
fake
Exploring this data frame reveals some issues we’d like to address before we begin the analysis. For example:
-
Some articles couldn’t be downloaded. When this happened, the url column contains NaN.
-
Some articles don’t have text (such as a web page with only video content). We drop these articles from our data frame.
1.*Unix epoch), so we need to convert them to pandas.Timestamp objects.
-
We’re interested in the base URL of a web page. However, the source field in the JSON file has many missing values compared to the url column. So we must extract the base URL using the full URL in the url column. For example, from dailybuzzlive.com/cannibals-arrested-florida/ we get dailybuzzlive.com.
-
Some articles were downloaded from an archival website (web.archive.org). When this happens, we want to extract the actual base URL from the original by removing the web.archive.org prefix.
-
We want to concatenate the title and text columns into a single content column that contains all of the text content of the article.
We can tackle these data issues using a combination of pandas functions and
regular expressions:
import re
# [1], [2]
def drop_nans(df):
return df[~(df['url'].isna() |
(df['text'].str.strip() == '') |
(df['title'].str.strip() == ''))]
# [3]
def parse_timestamps(df):
timestamp = pd.to_datetime(df['publish_date'], unit='s', errors='coerce')
return df.assign(timestamp=timestamp)
# [4], [5]
archive_prefix_re = re.compile(r'https://web.archive.org/web/\d+/')
site_prefix_re = re.compile(r'(https?://)?(www\.)?')
port_re = re.compile(r':\d+')
def url_basename(url):
if archive_prefix_re.match(url):
url = archive_prefix_re.sub('', url)
site = site_prefix_re.sub('', url).split('/')[0]
return port_re.sub('', site)
# [6]
def combine_content(df):
return df.assign(content=df['title'] + ' ' + df['text'])
def subset_df(df):
return df[['timestamp', 'baseurl', 'content', 'label']]
df = (df_raw
.pipe(drop_nans)
.reset_index(drop=True)
.assign(baseurl=lambda df: df['url'].apply(url_basename))
.pipe(parse_timestamps)
.pipe(combine_content)
.pipe(subset_df)
)
After data wrangling, we end up with the following data frame named df:
df.head(2)
timestamp
baseurl
content
label
0
2021-04-05 16:39:51
dailybuzzlive.com
Cannibals Arrested in Florida Claim Eating Hum...
fake
1
2016-01-01 23:17:43
houstonchronicle-tv.com
BREAKING: Trump fires Deputy Attorney General ...
fake
Now that we’ve loaded and cleaned the data, we can proceed to exploratory
data analysis.
