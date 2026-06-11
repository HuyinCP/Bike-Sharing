# Bus Scope

**Nguồn web:** [https://learningds.org/ch/05/bus_scope.html](https://learningds.org/ch/05/bus_scope.html)  
**Nguồn tải:** `github-ipynb` | `ch/05/bus_scope.ipynb`

---

```python
import sys
import os
if not any(path.endswith('textbook') for path in sys.path):
    sys.path.append(os.path.abspath('../../..'))
from textbook_utils import *
```

# Question and Scope

Our original question comes from the experience of a regular bus rider wondering why their bus is always late. We are not looking for actual reasons for its lateness, like a traffic jam or maintenance delay. Instead, we want to study patterns in the actual arrival times of buses at a stop, compared to their scheduled times. This information will help us better understand what it's like to wait for the bus. 

Bus lines differ across the world and even across a city, so we narrow our investigation to one bus stop in the city of Seattle.  The data we have are for the stops of Seattle's Rapid Ride lines C, D, and E at Third Avenue and Pike Street. The Washington State Transportation Center has provided times for all of the actual and scheduled stop times of these three bus lines between March 26 and May 27, 2016.

Considering our narrowed scope to buses at one particular stop over a two-month period and our access to all of the administrative data collected in this window of time, the population, access frame, and sample are one and the same.  Yet, we can imagine that our analysis might prove useful for other locations in and beyond Seattle and to other times of the year. If we are lucky, the ideas that we uncover, or the approach that we take, can be useful to others. For now, we keep a narrowed focus.

Let's take a look at these data to better understand their structure.
