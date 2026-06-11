# 11.7. Other Tools for Visualization

**Nguồn web:** [https://learningds.org/ch/11/viz_other_tools.html](https://learningds.org/ch/11/viz_other_tools.html)  
**Nguồn tải:** `web-html` | `ch/11/viz_other_tools`

---

# 11.7. Other Tools for Visualization#
There are many software packages and tools for creating data visualizations.
In this book, we primarily use plotly.
But it’s worth knowing about a few other commonly used tools.
In this section, we compare plotly to matplotlib and to grammar of graphics
tools.
## 11.7.1. matplotlib#
The library matplotlib is one of the first data
visualization tools created for Python. Because of this, it is widely used and
has a large ecosystem of packages. Notably, the built-in plotting methods for
pandas dataframes make plots using matplotlib. One popular package that
builds on top of matplotlib is called seaborn.
Compared to matplotlib alone, seaborn provides a much simpler API to create
statistical plots, like dot plots with confidence intervals. In fact,
seaborn’s API was used as an inspiration for plotly’s API. If you look at
plotly code and seaborn code side by side, you’ll find that the methods to
create basic plots use similar code.
One advantage of using matplotlib is its popularity. It’s relatively easy to
find help creating or fine-tuning plots online because many existing projects
use it. For this book, the main advantage of using plotly is that the plots
we create are interactive. Plots in matplotlib are usually static images,
which don’t allow for panning, zooming, or hovering over marks. Still, we
expect that matplotlib will continue to be used for data analyses. In fact,
several of the plots in this book were made using seaborn and matplotlib
because plotly doesn’t yet support all the plots we want to make.
## 11.7.2. Grammar of Graphics#
The grammar of graphics is a theory developed by Lee Wilkinson for creating data visualizations.
The basic idea is to use common building blocks for making plots.
For instance, a bar plot and a dot plot are nearly identical, except that
a bar plot draws rectangles and a dot plot draws points.
This idea is captured in the grammar of graphics, which would say that
a bar plot and a dot plot differ only in their “geometry” component.
The grammar of graphics is an elegant system that we can use to describe
nearly every kind of plot we wish to make.
This system is implemented in the popular plotting libraries ggplot2 for the
R programming language and Vega for JavaScript.
A Python package called Vega-Altair provides a way to create Vega plots using
Python, and we encourage interested readers to look over its documentation.
Using a grammar of graphics tool like Vega-Altair enables flexibility in visualizations.
And like plotly, altair also creates interactive visualizations.
However, the Python API for these tools can be less straightforward than
plotly’s API.
In this book, we don’t typically need plots outside of what plotly is capable
of creating, so we have opted for plotly’s simpler API.
There are many more plotting tools for Python that we’ve left out for brevity.
But for the purposes of this book, relying on plotly provides a useful
balance of interactivity and flexibility.
