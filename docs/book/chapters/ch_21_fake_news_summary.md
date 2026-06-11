# 21.5. Summary

**Nguồn web:** [https://learningds.org/ch/21/fake_news_summary.html](https://learningds.org/ch/21/fake_news_summary.html)  
**Nguồn tải:** `web-html` | `ch/21/fake_news_summary`

---

# 21.5. Summary#
We’re quickly approaching the end of the chapter and thus the end of the book. We started this book by talking about the data science lifecycle. Let’s take another look at the lifecycle, in Figure 21.2, to appreciate everything that you’ve learned.
Fig. 21.2 The four high-level steps of the data science lifecycle, each of which we’ve dove into throughout this book#
This case study stepped through each stage of the data science lifecycle:
-
Many data analyses begin with a research question. The case study we presented in this chapter started by asking whether we can create models to automatically detect fake news.
-
We obtained data by using code found online that scrapes web pages into JSON files. Since the data description was relatively minimal, we needed to clean the data to understand it. This included creating new features to indicate the presence or absence of certain words in the articles.
-
Our initial explorations identified possible words that might be useful for prediction.  After fitting simple models and exploring their precision and accuracy, we further transformed the articles using tf-idf to convert each news article into a normalized word vector.
-
We used the vectorized text as features in a logistic model, and we fitted the final model using regularization and cross-validation. Finally, we found the accuracy and precision of the fitted model on the test set.
When we write out the steps in the lifecycle like this, the steps seem to flow smoothly into each other. But reality is messy—as the diagram illustrates, real data analyses jump forward and backward between steps. For example, at the end of our case study, we discovered data cleaning questions that might motivate us to revisit earlier stages of the lifecycle. Although our model was quite accurate, the majority of the training data came from the 2016–2018 time period, so we have to carefully evaluate the model’s performance if we want to use it on articles published outside that time frame.
In essence, it’s important to keep the entire lifecycle in mind at each stage
of a data analysis. As a data scientist, you will be asked to justify your
decisions, which means that you need to deeply understand your research
question and data. To develop this understanding, the principles and techniques
in this book equip you with a foundational set of skills. As you go forward
into your data science journey, we recommend that you continue to expand your
skills by:
-
Revisiting a case study from this book. Start by replicating our analysis,
then dive deeper into questions that you have about the data.
-
Conducting an independent data analysis. Pose a research question you’re
interested in, find relevant data from the web, and analyze the data to see
how well the data matched your expectations. Doing this will give you
firsthand experience with the entire data science lifecycle.
-
Taking a deep dive into a topic. We’ve provided many in-depth resources in
the Additional Material appendix. Take the resource that seems most
interesting to you and learn more about it.
The world needs people like you who can use data to make conclusions, so we
sincerely hope that you’ll use these skills to help others make effective
strategies, better products, and informed decisions.
