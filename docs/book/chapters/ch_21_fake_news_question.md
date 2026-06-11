# 21.1. Question and Scope

**Nguồn web:** [https://learningds.org/ch/21/fake_news_question.html](https://learningds.org/ch/21/fake_news_question.html)  
**Nguồn tải:** `web-html` | `ch/21/fake_news_question`

---

# 21.1. Question and Scope#
Our initial research question is: can we automatically detect fake news? To refine this question, we consider the kind of information that we might use to build a model for detecting fake news. If we have hand-classified news stories where people have read each story and determined whether it is fake or not, then our question becomes: can we build a model to accurately predict whether a news story is fake based on its content?
To address this question, we can use the FakeNewsNet data repository as described in Shu et al. This repository contains content from news and social media websites, as well as metadata like user engagement metrics.
For simplicity, we only look at the dataset’s political news articles.
This subset of the data includes only articles that
were fact-checked by Politifact, a
nonpartisan organization with a good reputation.
Each article in the dataset has a “real” or “fake” label based
on Politifact’s evaluation, which we use as the ground truth.
Politifact uses a nonrandom sampling method to select articles to fact-check. According to its website, Politifact’s journalists select the “most newsworthy and significant” claims each day. Politifact started in 2007 and the repository was published in 2020, so most of the articles were published between 2007 and 2020.
Summarizing this information, we determine that the target population consists of all political news stories published online in the time period from 2007 to 2020 (we would also want to list the sources of the stories). The access frame is determined by Politifact’s identification of the most newsworthy claims of the day. So the main sources of bias for this data include:
Coverage bias
The news outlets are limited to those that Politifact monitored, which may miss arcane or short-lived sites.
Selection bias
The data are limited to articles Politifact decided were interesting enough to fact-check, which means that articles might skew toward ones that are both widely shared and controversial.
Measurement bias
Whether a story should be labeled “fake” or “real” is determined by one organization (Politifact) and reflects the biases, unintentional or otherwise, that the organization has in its fact-checking methodology.
Drift
Since we only have articles published between 2007 and 2020, there is likely to be drift in the content. Topics are popularized and faked in rapidly evolving news trends.
We will keep these limitations of the data in mind as we begin to wrangle the data into a form that we can analyze.
