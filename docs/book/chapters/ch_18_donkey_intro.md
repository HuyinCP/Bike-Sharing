# 18. Case Study: How to Weigh a Donkey

**Nguồn web:** [https://learningds.org/ch/18/donkey_intro.html](https://learningds.org/ch/18/donkey_intro.html)  
**Nguồn tải:** `web-html` | `ch/18/donkey_intro`

---

# 18. Case Study: How to Weigh a Donkey#
Donkeys play important roles in rural Kenya. People need them to transport crops, water, and people and to plow fields.
When a donkey gets sick, the veterinarian needs to figure out how much the donkey
weighs in order to prescribe the right amount of medicine.
But many vets in rural Kenya don’t have access to a scale, so they need to guess the donkey’s weight.
Too little medicine can allow an infection to reemerge; too much medicine can cause a harmful overdose.
There are over 1.8 million donkeys in Kenya, so it’s important to have
a simple, accurate way to estimate the weight of a donkey.
In this case study, we follow the work of Kate Milner and Jonathan Rougier to create a model that veterinarians in the Kenyan countryside can use to make accurate estimates of a donkey’s weight.
As usual, we walk through the steps of the data science lifecycle, but this time our work departs from the basics covered so far in this book. You can think of this case study as an opportunity to reflect on many of the core principles of working with data and to understand how they can be extended to address the context of the situation. We directly evaluate sources of measurement error, design a special loss function that reflects the concern about an overdose, build a model while keeping applicability utmost in mind, and evaluate model predictions using special criteria that are relative to the donkey’s size.
We begin with the scope of the data.
