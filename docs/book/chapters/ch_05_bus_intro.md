# 5. Case Study: Why Is My Bus Always Late?

**Nguồn web:** [https://learningds.org/ch/05/bus_intro.html](https://learningds.org/ch/05/bus_intro.html)  
**Nguồn tải:** `web-html` | `ch/05/bus_intro`

---

# 5. Case Study: Why Is My Bus Always Late?#
Jake VanderPlas’s blog, Pythonic Perambulations, offers a great example of what it’s like to be a modern data scientist. As data scientists, we see data in our work, daily routines, and personal lives, and we tend to be curious about what insights these data might bring to our understanding of the world. In this first case study, we borrow from one of the posts on Pythonic Perambulations, “The Waiting Time Paradox, or, Why Is My Bus Always Late?” to model waiting for a bus on a street corner in Seattle. We touch on each stage of the data lifecycle, but in this first case study, our focus is on the process of how to think about the question, data, and model, rather than on data structures and modeling techniques. A constant model and simulation study get us a long way toward understanding the issues.
VanderPlas’s post was inspired by his experience waiting for the bus. The wait always seemed longer than expected. This experience did not match the reasoning that if a bus comes every 10 minutes and you arrive at the stop at a random time, then, on average, the wait should be about 5 minutes. Armed with data provided by the Washington State Transportation Center, the author was able to investigate this phenomenon. We do the same.
We apply concepts introduced in earlier chapters, beginning with the general question, why is my bus always late, and refining this question to one that is closer to our goal and that we can investigate with data. We then consider the data scope, such as how these data were collected and potential sources of biases, and we prepare the data for analysis. Our understanding of the data scope helps us design a model for waiting at a bus stop, which we simulate to study this phenomenon.
