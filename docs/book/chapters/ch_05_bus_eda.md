# Bus Eda

**Nguồn web:** [https://learningds.org/ch/05/bus_eda.html](https://learningds.org/ch/05/bus_eda.html)  
**Nguồn tải:** `github-ipynb` | `ch/05/bus_eda.ipynb`

---

```python
# Reference: https://jupyterbook.org/interactive/hiding.html
# Use {hide, remove}-{input, output, cell} tags to hiding content

import sys
import os
if not any(path.endswith('textbook') for path in sys.path):
    sys.path.append(os.path.abspath('../../..'))
from textbook_utils import *
```

```python
def clean_stops(bus):
    return bus.assign(
        route=bus["RTE"].replace({673: "C", 674: "D", 675: "E"}),
        direction=bus["DIR"].replace({"N": "northbound", "S": "southbound"}),
    )

def compute_mins_late(bus):
    bus = bus.assign(
        scheduled=pd.to_datetime(bus["OPD_DATE"] + " " + bus["SCH_STOP_TM"]),
        actual=pd.to_datetime(bus["OPD_DATE"] + " " + bus["ACT_STOP_TM"]),
    )
    # if scheduled & actual span midnight, then the actual day needs to be
    # adjusted
    minute = pd.Timedelta("1 minute")
    hour = pd.Timedelta("1 hour")
    diff_hrs = (bus["actual"] - bus["scheduled"]) / hour
    bus.loc[diff_hrs > 20, "actual"] -= 24 * hour
    bus.loc[diff_hrs < -20, "actual"] += 24 * hour
    return bus.assign(minutes_late=(bus["actual"] - bus["scheduled"]) / minute)

bus = (
    pd.read_csv("data/seattle_bus_times.csv")
    .dropna(axis=0, how="any")
    .pipe(clean_stops)
    .pipe(compute_mins_late)
    [['route', 'direction', 'scheduled', 'actual', 'minutes_late']]
)
```

# Exploring Bus Times

We learned a lot about the data as we cleaned and simplified it, but before we begin to model wait time, we want to dig deeper to better understand the phenomenon of bus lateness. We narrowed our focus to the bus activity at one stop (Third Avenue and Pike Street) over a two-month period. And we saw that the distribution of the lateness of a bus is skewed to the right, with some buses being very late indeed. In this exploratory phase, we might ask:

+ Does the distribution of lateness look the same for all three bus lines?
+ Does it matter whether the bus is traveling north or south?
+ How does the time of day relate to how late the bus is?
+ Are the buses scheduled to arrive at regular intervals throughout the day? 

Answering these questions helps us better determine how to model. 

Recall from {numref}`Chapter %s <ch:modeling>` that we found the median time a bus was late was 3/4 of a minute. But this doesn't match the median we calculated for all bus routes and directions (1/2 a minute). Let's check whether that could be due to the focus on northbound line C buses in that chapter. Let's create histograms of lateness for each of the six combinations of bus line and direction to address this question and the first two questions on our list:

```python
fig = px.histogram(bus, x='minutes_late', 
                   histnorm='probability density', nbins=200,
                   facet_row='direction', facet_col='route',
                   facet_row_spacing=0.1,
                   labels={'minutes_late':'Minutes late'},
                   width=550, height=400)

fig.update_xaxes(range=[-12, 25])
fig.update_yaxes(range=[0, 0.3], title="")
margin(fig, t=25)
fig.show()
```

The scale on the y-axis is proportion (or density). This scale makes it easier to compare the histograms since we are not misled by different counts in the groups. The range on the x-axis is the same across the six plots, making it easier to detect the different center and spread of the distributions. (These notions are described in {numref}`Chapter %s <ch:viz>`.)

The northbound and southbound distributions are different for each line. When we dig deeper into the context, we learn that line C originates in the north and the other two lines originate in the south. The histograms imply there is greater variability in arrival times in the second half of the bus routes, which makes sense to us since delays get compounded as the day progresses.

Next, to explore lateness by time of day, we need to derive a new quantity: the hour of the day that the bus is scheduled to arrive. Given the variation in route and direction that we just saw in bus lateness, we  again create separate plots for each route and direction:

```python
bus['hour_of_day'] = bus['scheduled'].dt.hour

fig = px.box(bus, y='minutes_late', x='hour_of_day',                 
             facet_row='direction', facet_col='route',
             labels={'minutes_late':'Minutes late',
                    'hour_of_day':'Hour of the day'},
             width=600, height=400)

fig.update_yaxes(range=[-12, 50])
margin(fig, t=25)
fig.show()
```

Indeed, there does appear to be a rush-hour effect, and it seems worse for the evening rush hour compared to the morning. The northbound C line looks to be the most impacted.

Lastly, to examine the scheduled frequency of the buses, we need to compute the intervals between scheduled bus times. We create a new column in our table that contains the time between the scheduled arrival times for the northbound C buses:

```python
minute = pd.Timedelta('1 minute')
bus_c_n = (
    bus[(bus['route'] == 'C') & (bus['direction'] == 'northbound')]
    .sort_values('scheduled')
    .assign(sched_inter=lambda x: x['scheduled'].diff() / minute)
)
bus_c_n.head(3)
```

Let's examine a histogram of the distribution of inter-arrival times of these buses:

```python
fig = px.histogram(bus_c_n, x='sched_inter', 
                   title="Bus line C, northbound",
                   width=450, height=300)

fig.update_xaxes(range=[0, 40], title="Time between consecutive buses")
fig.update_layout(margin=dict(t=40))
```

We see that the buses are scheduled to arrive at different intervals throughout the day. In this two-month period, about 1,500 of the buses are scheduled to arrive 12 minutes apart and about 1,400 are supposed to arrive 15 minutes after the previous bus. 

We have learned a lot in our exploration of the data and are in a better position to fit a model. Most notably, if we want to get a clear picture of the experience of waiting for a bus, we need to take into account the scheduled interval between buses, as well as the bus line and direction.
