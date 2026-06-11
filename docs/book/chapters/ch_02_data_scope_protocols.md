# 2.3. Instruments and Protocols

**Nguồn web:** [https://learningds.org/ch/02/data_scope_protocols.html](https://learningds.org/ch/02/data_scope_protocols.html)  
**Nguồn tải:** `web-html` | `ch/02/data_scope_protocols`

---

# 2.3. Instruments and Protocols#
When we consider the scope of the data, we also consider the instrument being used to take the measurements and the procedure for taking measurements, which we call the protocol. For a survey, the instrument is typically a questionnaire that an individual in the sample answers. The protocol for a survey includes how the sample is chosen, how nonrespondents are followed up on, interviewer training, protections for confidentiality, and so on.
Good instruments and protocols are important to all kinds of data collection. If we want to measure a natural phenomenon, such as carbon dioxide in the atmosphere, we need to quantify the accuracy of the instrument. The protocol for calibrating the instrument and taking measurements is vital to obtaining accurate measurements. Instruments can go out of alignment and measurements can drift over time, leading to poor, highly inaccurate measurements.
Protocols are also critical in experiments. Ideally, any factor that can influence the outcome of the experiment is controlled. For example, temperature, time of day, confidentiality of a medical record, and even the order in which measurements are taken need to be consistent to rule out potential effects from these factors getting in the way.
With digital traces, the algorithms used to support online activity are dynamic and continually reengineered. For example, Google’s search algorithms are continually tweaked to improve user service and advertising revenue. Changes to the search algorithms can impact the data generated from the searches, which in turn impact systems built from these data, such as the Google Flu Trend tracking system. This changing environment can make it untenable to maintain data collection protocols and difficult to replicate findings.
Many data science projects involve linking data together from multiple sources. Each source should be examined through this data-scope construct, and any difference across sources should be considered. Additionally, matching algorithms used to combine data from multiple sources need to be clearly understood so that populations and frames from the sources can be compared.
Measurements from an instrument taken to study a natural phenomenon can be cast in the scope diagram of  a target, access frame, and sample. This approach is helpful in understanding the instrument’s accuracy.
