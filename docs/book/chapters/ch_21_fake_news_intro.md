# 21. Case Study: Detecting Fake News

**Nguồn web:** [https://learningds.org/ch/21/fake_news_intro.html](https://learningds.org/ch/21/fake_news_intro.html)  
**Nguồn tải:** `web-html` | `ch/21/fake_news_intro`

---

# 21. Case Study: Detecting Fake News#
Fake news—false information created in order to deceive others—is an
important issue because it can harm people.
For example, the social media post in
Figure 21.1
confidently stated that hand sanitizer doesn’t work on coronaviruses.
Though factually incorrect, it spread through social media anyway:
it was shared nearly 100,000 times and was likely seen by millions of people.
Fig. 21.1 A popular post on Twitter from March 2020 falsely claimed that sanitizer doesn’t kill coronaviruses#
We might wonder whether we can automatically detect fake news without having to read the stories.
For this case study, we go through the steps of the data science lifecycle.
We start by refining our research question and obtaining a dataset of news
articles and labels.
Then we wrangle and transform the data.
Next, we explore the data to understand its content and
devise features to use for modeling.
Finally, we build models using logistic regression to predict whether news articles are real or fake, and evaluate their performance.
We’ve included this case study because it lets us reiterate several important
ideas in data science.
First, natural language data appear often, and even basic techniques can enable
useful analyses.
Second, model selection is an important part of data analysis, and in this case
study we apply what we’ve learned about cross-validation, the bias–variance trade-off, and regularization.
Finally, even models that perform well on the test set might have inherent
limitations when we try to use them in practice, as we will soon see.
Let’s start by refining our research question and understanding the scope of
our data.
