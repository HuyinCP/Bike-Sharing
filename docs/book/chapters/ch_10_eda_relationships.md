# 10.3. What to Look For in a Relationship

**Nguồn web:** [https://learningds.org/ch/10/eda_relationships.html](https://learningds.org/ch/10/eda_relationships.html)  
**Nguồn tải:** `web-html` | `ch/10/eda_relationships`

---

# 10.3. What to Look For in a Relationship#
When we investigate multiple variables, we examine the relationships between
them, in addition to their distributions. In this section, we
consider pairs of features and describe what to look for.
Table 10.3 provides guidelines for the type of plot to make
based on the feature types.
For two features, the combination of types (both quantitative, both qualitative, or a mix) matters.
We consider each combination in turn.
## 10.3.1. Two Quantitative Features#
If both features are quantitative, then we often
examine their relationship with a scatter plot.
Each point in a scatter plot
marks the position of a pair of values for an observation.
So we can think of a scatter plot as a two-dimensional rug plot.
With scatter plots, we look for linear and simple nonlinear relationships, and we examine the strength of the relationships.
We also look to see if a transformation of one or the other or both features leads to a linear relationship.
The following scatter plot displays the weight and height of dog breeds (both are
quantitative):
px.scatter(dogs, x='height', y='weight',
marginal_x="rug", marginal_y="rug",
labels={'height':'Height (cm)', 'weight':'Weight (kg)'},
width=350, height=250)
We observe that dogs that are above average in height tend to be
above average in weight. This relationship appears nonlinear: the change in weight for taller dogs grows faster than for shorter dogs. Indeed, that makes sense if we think of a dog as basically shaped like a box: for similarly proportioned boxes, the weight of the contents of the box has a cubic relationship to its length.
It’s important to note that two univariate plots are missing information found in a bivariate plot—information about how the two features vary together.
Practically, histograms for two quantitative features do not contain enough information to create a scatter plot of the features. We must exercise caution and not read too much into a pair of univariate plots. Instead, we need to use one of the plots listed in the appropriate row of
Table 10.3
(scatter plot, smooth curve, contour plot, heat map,
quantile-quantile plot) to get a sense of
the relationship between two quantitative features.
When one feature is numeric and the other qualitative, Table 10.3 makes different recommendations. We describe them next.
## 10.3.2. One Qualitative and One Quantitative Variable#
To examine the relationship between a quantitative and a qualitative
feature, we often use the qualitative feature to divide the data into groups
and compare the distribution of the quantitative feature across these groups.
For example, we can compare the distribution of height for small, medium,
and large dog breeds with three overlaid density curves:
fig = plt.figure(figsize=(6, 3))
ax = sns.kdeplot(data=dogs, x='height', hue='size')
ax.set(xlabel='Height (cm)', ylabel='')
ax.get_legend().set_title("Size")
lss = ['-', '--', '-.']
handles = ax.legend_.legend_handles[::-1]
for line, ls, handle in zip(ax.lines, lss, handles):
line.set_linestyle(ls)
handle.set_ls(ls)
We see that the distribution of height for the
small and medium breeds both appear bimodal, with the left mode the larger
in each group. Also, the small and medium groups have a larger spread in
height than the large group of breeds.
Side-by-side box plots offer a similar comparison of distributions across
groups. The box plot offers a simpler approach that can give a crude understanding of a distribution. Likewise, violin
plots sketch density curves along an axis for each group. The curve is flipped to create a symmetric “violin” shape. The violin plot aims
to bridge the gap between the density curve and box plot. We create box plots (left) and violin plots (right) for the height of breeds given the size labeling:
fig = make_subplots(rows=1, cols=2)
fig.add_trace(go.Box(x=dogs["size"], y=dogs["height"]), row=1, col=1)
fig.add_trace(go.Violin(x=dogs["size"], y=dogs["height"]), row=1, col=2)
fig.update_yaxes(range=[0, 90])
fig.update_yaxes(title="Height (cm)", row=1, col=1)
fig.update_xaxes(
categoryarray=["small", "medium", "large"], categoryorder="array",
title = "Size"
)
fig.update_layout(showlegend=False, width=550, height=250)
fig.show()
The three box plots of height, one for each size of dog, make it clear that the size categorization is based on
height because there is almost no overlap in height ranges for the groups. (This was
not evident in the density curves due to the smoothing.) What we don’t see in
these box plots is the bimodality in the small and medium groups, but we can
still see that the large dogs have a narrower spread compared to
the other two groups.
Box plots (also known as box-and-whisker plots) give a visual summary
of a few important statistics of a distribution.
The box denotes the 25th percentile, median, and 75th percentile, the whiskers show the tails, and unusually large or small values are also plotted.
Box plots cannot reveal as much shape as a histogram or density curve.
They primarily show symmetry and skew, long/short tails, and unusually
large/small values (also known as outliers).
Figure 10.2 is a visual explanation of the parts of a box
plot. Asymmetry is evident from the median not being in the middle of the box, the sizes of the tails are shown by the length of the whiskers, and outliers are shown by the points that appear beyond the whiskers. The maximum is considered an outlier because it appears beyond the whisker on the right.
Fig. 10.2 Diagram of a box plot with the summary statistics labeled#
When we examine the relationship between two qualitative features, our focus is on proportions, as we explain next.
## 10.3.3. Two Qualitative Features#
With two qualitative features, we often compare the distribution of one feature
across subgroups defined by the other feature. In effect, we hold one feature constant
and plot the distribution of the other one. To do this, we can use some of the same plots
we used to display the distribution of one qualitative feature, such as a line plot or
bar plot.
As an example, let’s examine the relationship between the suitability of a breed for children and the size of the breed.
To examine the relationship between these two qualitative features, we calculate three sets of
proportions (one each for low, medium, and high suitability).
Within each suitability category, we find  the proportion of small, medium, and large dogs.
These proportions are displayed in the following table. Notice that each column sums to 1 (equivalent to 100%):
def proportions(series):
return series / sum(series)
counts = (dogs.groupby(['kids', 'size'])
.size()
.rename('count')
)
prop_table = (counts
.unstack(level=1)
.reindex(['high', 'medium', 'low'])
.apply(proportions, axis=1)
)
prop_table_t= prop_table.transpose()
prop_table_t
kids
high
medium
low
size
large
0.37
0.29
0.1
medium
0.36
0.34
0.2
small
0.27
0.37
0.7
The line plot that follows provides a visualization of these proportions.
There is one “line” (set of connected dots) for each suitability level.
The connected dots give the breakdown of size within a suitability category.
We see that breeds with low suitability for kids are primarily small:
fig = px.line(prop_table_t, y=prop_table_t.columns,
x=prop_table_t.index, line_dash='kids',
markers=True, width=500, height=250)
fig.update_layout(
yaxis_title="proportion", xaxis_title="Size",
legend_title="Suitability <br>for children"
)
We can also present these proportions as a collection of side-by-side bar plots as shown here:
fig = px.bar(prop_table_t, y=prop_table_t.columns, x=prop_table_t.index,
barmode='group', width=500, height=250)
fig.update_layout(
yaxis_title="proportion", xaxis_title="Size",
legend_title="Suitability <br>for children"
)
So far, we’ve covered visualizations that incorporate one or two features.
In the next section, we discuss visualizations that incorporate more than two features.
