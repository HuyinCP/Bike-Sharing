# 10.7. Summary

**Nguồn web:** [https://learningds.org/ch/10/eda_summary.html](https://learningds.org/ch/10/eda_summary.html)  
**Nguồn tải:** `web-html` | `ch/10/eda_summary`

---

# 10.7. Summary#
In this chapter, we introduced the nominal, ordinal, and numerical feature
types and their importance for data analysis. When presented with a dataset, we
demonstrated how to consult the data dictionary and the data itself to
determine the feature types for each column. We also explained how the storage
type is not to be confused with feature type. Since much of EDA is carried out
with statistical graphs, we described how to recognize and interpret the shapes
and patterns that emerge and how to connect these to the data being plotted. Finally,
we provided guidelines for how you might conduct an EDA, and provided an
example.
One approach that you may find helpful in developing your intuition about
distributions and relationships of features is to make a
guess about what you will see before you make the plot. Try to sketch
or describe what you think the shape of distribution will be, and then make the plot.
For example, variables that have a natural lower/upper bound on their
values tend to have a long tail on the opposite of the bound. The distribution of income
(bounded below by 0) tends to have a long right tail, and exam scores (bounded
above by 100) tend to have a long left tail. You can make similar guesses for the
shape of a relationship. We saw that price and house size had nearly a log–log linear relationship.
As you gain intuition about shapes, it becomes easier to carry out an EDA; you can more easily identify when a plot shows a surprising shape.
Our focus in this chapter was on “reading” visualizations. In Chapter 11, we provide style guidelines for how to
create informative, effective, and beautiful graphs. Many of the ideas in that
chapter were followed here, but we have not called attention to them.
