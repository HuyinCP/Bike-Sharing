# Bus Summary

**Nguồn web:** [https://learningds.org/ch/05/bus_summary.html](https://learningds.org/ch/05/bus_summary.html)  
**Nguồn tải:** `github-ipynb` | `ch/05/bus_summary.ipynb`

---

```python
import sys
import os
if not any(path.endswith('textbook') for path in sys.path):
    sys.path.append(os.path.abspath('../../..'))
from textbook_utils import *
```

(sec:bus_summary)=
# Summary

In our first case study, we have traversed the full data life modeling. It might strike you how such a simple question is not immediately answerable with the data collected. We needed to combine the data of scheduled and actual arrival times of buses with a simulation study of riders arriving at the bus stop at random times to uncover the riders' waiting experience.    

This simulation simplified many of the real patterns in bus riding. We focused on one bus line traveling in one direction with buses arriving at 12-minute intervals. Further, the exploration of the data revealed that the patterns in lateness correlated with the time of day, which we have not accounted for in our analysis. Nonetheless, our findings can still be useful. For example, they confirm that the typical wait time is longer than half the scheduled interval. And the distribution of wait times has a long right tail, meaning a rider's experience may well be impacted by the variability in the process.

We also saw how deriving new quantities, such as how late a bus is and the time between buses, and exploring the data can be useful in modeling. Our histograms showed that the particular line and direction of the bus matter and they need to be accounted for. We also discovered that the schedules change throughout the day, with many buses arriving 10, 12, and 15 minutes after another, and some arriving more frequently or more separated. This observation further informed the modeling stage.    

Finally, we used data tools, such as the `pandas` and `plotly` libraries, that will be covered in later chapters. Our focus here was not on how to manipulate tables or how to create a plot. Instead, we focused on the lifecycle, connecting questions to data to modeling to conclusions. In the next chapter, we turn to the practicalities of working with data tables.
