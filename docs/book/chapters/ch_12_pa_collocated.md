# 12.2. Finding Collocated Sensors

**Nguồn web:** [https://learningds.org/ch/12/pa_collocated.html](https://learningds.org/ch/12/pa_collocated.html)  
**Nguồn tải:** `web-html` | `ch/12/pa_collocated`

---

# 12.2. Finding Collocated Sensors#
Our analysis begins by finding collocated pairs of AQS and PurpleAir sensors—sensors that are placed essentially next to each other.
This step is important because it lets us reduce the effects of other variables that might cause differences in sensor readings.
Consider what would happen if we compared an AQS sensor placed in a park with a PurpleAir sensor placed along a busy freeway.
The two sensors would have different readings, in part because the sensors are exposed to different environments.
Ensuring that sensors are truly collocated lets us claim the differences in sensor readings are due to how the sensors are built and to small, localized air fluctuations, rather than
other potential confounding variables.
Barkjohn’s analysis conducted by the EPA group found pairs of AQS and PurpleAir sensors that
are installed within 50 meters of each other.
The group contacted each AQS site to see whether the PurpleAir sensor was also maintained there.
This extra effort gave them confidence that their sensor pairs were truly collocated.
In this section, we explore and clean location data from AQS and PurpleAir.
Then we perform a join of sorts to construct a list of potentially collocated sensors.
We won’t contact AQS sites ourselves;
instead, we proceed in later sections with Barkjohn’s list of confirmed
collocated sensors.
We downloaded a list of AQS and PurpleAir sensors and saved the data in the files
data/list_of_aqs_sites.csv
and data/list_of_purpleair_sensors.json.
Let’s begin by reading these files into pandas dataframes.
First, we check file sizes to see whether they are reasonable to load into memory:
!ls -lLh data/list_of*
-rw-r--r--  1 sam  staff   4.8M Oct 27 16:54 data/list_of_aqs_sites.csv
-rw-r--r--  1 sam  staff   3.8M Oct 22 16:10 data/list_of_purpleair_sensors.json
Both files are relatively small. Let’s start with the list of AQS sites.
## 12.2.1. Wrangling the List of AQS Sites#
We have filtered the AQS map of sites to show only the AQS sites that measure PM2.5, and then downloaded the list of sites as a CSV file using the map’s web app. Now we can load it into a pandas dataframe.:
aqs_sites_full = pd.read_csv('data/list_of_aqs_sites.csv')
aqs_sites_full.shape
(1333, 28)
There are 28 columns in the table. Let’s check the column names:
aqs_sites_full.columns
Index(['AQS_Site_ID', 'POC', 'State', 'City', 'CBSA', 'Local_Site_Name',
'Address', 'Datum', 'Latitude', 'Longitude', 'LatLon_Accuracy_meters',
'Elevation_meters_MSL', 'Monitor_Start_Date', 'Last_Sample_Date',
'Active', 'Measurement_Scale', 'Measurement_Scale_Definition',
'Sample_Duration', 'Sample_Collection_Frequency',
'Sample_Collection_Method', 'Sample_Analysis_Method',
'Method_Reference_ID', 'FRMFEM', 'Monitor_Type', 'Reporting_Agency',
'Parameter_Name', 'Annual_URLs', 'Daily_URLs'],
dtype='object')
To find out which columns are most useful for us, we reference the data dictionary that the AQS provides on its website.
There we confirm that the data table contains information about the AQS sites.
So we might expect the granularity corresponds to an AQS site; meaning each row represents a single site
and the column labeled AQS_Site_ID is the primary key. We can confirm this with a count of records for each ID:
aqs_sites_full['AQS_Site_ID'].value_counts()
06-071-0306    4
19-163-0015    4
39-061-0014    4
..
46-103-0020    1
19-177-0006    1
51-680-0015    1
Name: AQS_Site_ID, Length: 921, dtype: int64
It looks like some sites appear multiple times in this dataframe.
Unfortunately, this means that the granularity is finer than the individual site level.
To figure out why sites are duplicated, let’s take a closer look at the rows for one duplicated site:
dup_site = aqs_sites_full.query("AQS_Site_ID == '19-163-0015'")
We select a few columns to examine based on their names—those that sound like they might shed some light on the reason for duplicates:
some_cols = ['POC', 'Monitor_Start_Date',
'Last_Sample_Date', 'Sample_Collection_Method']
dup_site[some_cols]
POC
Monitor_Start_Date
Last_Sample_Date
Sample_Collection_Method
458
1
1/27/1999
8/31/2021
R & P Model 2025 PM-2.5 Sequential Air Sampler...
459
2
2/9/2013
8/26/2021
R & P Model 2025 PM-2.5 Sequential Air Sampler...
460
3
1/1/2019
9/30/2021
Teledyne T640 at 5.0 LPM
461
4
1/1/2019
9/30/2021
Teledyne T640 at 5.0 LPM
The POC column looks to be useful for distinguishing between rows in the table. The data dictionary  states this about the column:
This is the “Parameter Occurrence Code” used to distinguish different instruments that measure the same parameter at the same site.
So, the site 19-163-0015 has four instruments that all
measure PM2.5. The granularity of the dataframe is at the level of a single instrument.
Since our aim is to match AQS and PurpleAir sensors,
we can adjust the granularity by selecting one instrument from each AQS site.
To do this, we group rows according to site ID, then take the first row in each group:
def rollup_dup_sites(df):
return (
df.groupby('AQS_Site_ID')
.first()
.reset_index()
)
aqs_sites = (aqs_sites_full
.pipe(rollup_dup_sites))
aqs_sites.shape
(921, 28)
Now the number of rows matches the number of unique IDs.
To match AQS sites with PurpleAir sensors, we only need the site ID, latitude, and longitude.
So we further adjust the structure and keep only those columns:
def cols_aqs(df):
subset = df[['AQS_Site_ID', 'Latitude', 'Longitude']]
subset.columns = ['site_id', 'lat', 'lon']
return subset
aqs_sites = (aqs_sites_full
.pipe(rollup_dup_sites)
.pipe(cols_aqs))
Now the aqs_sites dataframe is ready, and we move to the PurpleAir sites.
## 12.2.2. Wrangling the List of PurpleAir Sites#
Unlike the AQS sites, the file containing PurpleAir sensor data comes in a
JSON format. We address this format in more detail in Chapter 14. For now, we use shell tools (see Chapter 8) to peak at the  file contents:
!head data/list_of_purpleair_sensors.json | cut -c 1-60
{"version":"7.0.30",
"fields":
["ID","pm","pm_cf_1","pm_atm","age","pm_0","pm_1","pm_2","pm
"data":[
[20,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,97,0.0,0.0,0.0
[47,null,null,null,4951,null,null,null,null,null,null,null,9
[53,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,1.2,5.2,6.0,97,0.0,0.5,702
[74,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,97,0.0,0.0,0.0
[77,9.8,9.8,9.8,1,9.8,10.7,11.0,11.2,13.8,15.1,15.5,97,9.7,9
[81,6.5,6.5,6.5,0,6.5,6.1,6.1,6.6,8.1,8.3,9.7,97,5.9,6.8,405
From the first few lines of the file, we can guess that the data are
stored in the "data" key and the column labels in the "fields" key.
We can use Python’s json library to read in the file as a Python dict:
import json
with open('data/list_of_purpleair_sensors.json') as f:
pa_json = json.load(f)
list(pa_json.keys())
['version', 'fields', 'data', 'count']
We can create a dataframe from the values in data and label the columns with the content of fields:
pa_sites_full = pd.DataFrame(pa_json['data'], columns=pa_json['fields'])
pa_sites_full.head()
ID
pm
pm_cf_1
pm_atm
...
Voc
Ozone1
Adc
CH
0
20
0.0
0.0
0.0
...
NaN
NaN
0.01
1
1
47
NaN
NaN
NaN
...
NaN
0.72
0.72
0
2
53
0.0
0.0
0.0
...
NaN
NaN
0.00
1
3
74
0.0
0.0
0.0
...
NaN
NaN
0.05
1
4
77
9.8
9.8
9.8
...
NaN
NaN
0.01
1
5 rows × 36 columns
Like the AQS data, there are many more columns in this dataframe  than we need:
pa_sites_full.columns
Index(['ID', 'pm', 'pm_cf_1', 'pm_atm', 'age', 'pm_0', 'pm_1', 'pm_2', 'pm_3',
'pm_4', 'pm_5', 'pm_6', 'conf', 'pm1', 'pm_10', 'p1', 'p2', 'p3', 'p4',
'p5', 'p6', 'Humidity', 'Temperature', 'Pressure', 'Elevation', 'Type',
'Label', 'Lat', 'Lon', 'Icon', 'isOwner', 'Flags', 'Voc', 'Ozone1',
'Adc', 'CH'],
dtype='object')
In this case, we can guess that the columns we’re most interested in are the
sensor IDs (ID), sensor labels (Label), latitude (Lat), and longitude (Lon).
But we did consult the data dictionary on the PurpleAir website to double-check.
Now let’s check the ID column for duplicates, as we did for the AQS data:
pa_sites_full['ID'].value_counts()[:3]
85829     1
117575    1
118195    1
Name: ID, dtype: int64
Since the value_counts() method lists the counts in descending order, we can see
that every ID was included only once. So we have verified the granularity is at the individual sensor level.
Next, we keep only the columns needed to match sensor locations from the two sources:
def cols_pa(df):
subset = df[['ID', 'Label', 'Lat', 'Lon']]
subset.columns = ['id', 'label', 'lat', 'lon']
return subset
pa_sites = (pa_sites_full
.pipe(cols_pa))
pa_sites.shape
(23138, 4)
Notice there are tens of thousands more PurpleAir sensors than AQS sensors.
Our next task is to find the PurpleAir sensor close to each AQS sensor.
## 12.2.3. Matching AQS and PurpleAir Sensors#
Our goal is to match sensors in the two dataframes by finding a PurpleAir sensor near each AQS instrument.
We consider near to mean within 50 meters.
This kind of matching is a bit more challenging than the joins we’ve seen thus far.
For instance, the naive approach to use the merge method of pandas fails us:
aqs_sites.merge(pa_sites, left_on=['lat', 'lon'], right_on=['lat', 'lon'])
site_id
lat
lon
id
label
0
06-111-1004
34.45
-119.23
48393
VCAPCD OJ
We cannot simply match instruments with the exact same latitude and longitude;
we need to find the PurpleAir sites that are close enough to the AQS instrument.
To figure out how far apart two locations are, we use a basic approximation: 111,111 meters in the
north–south direction roughly equals one degree of latitude, and 111,111 * cos(latitude) in the east–west direction
corresponds to one degree of longitude.1
So we can find the latitude and longitude ranges that correspond to 25 meters
in each direction (to make a 50-by-50 meter rectangle around each point):
magic_meters_per_lat = 111_111
offset_in_m = 25
offset_in_lat = offset_in_m / magic_meters_per_lat
offset_in_lat
0.000225000225000225
To simplify even more, we use the median latitude for the AQS sites:
median_latitude = aqs_sites['lat'].median()
magic_meters_per_lon = 111_111 * np.cos(np.radians(median_latitude))
offset_in_lon = offset_in_m / magic_meters_per_lon
offset_in_lon
0.000291515219937587
Now we can match coordinates to within the offset_in_lat and offset_in_lon.
Doing this in SQL is much easier than in pandas, so we
push the tables into a temporary SQLite database, then run a query to read
the tables back into a dataframe:
import sqlalchemy
db = sqlalchemy.create_engine('sqlite://')
aqs_sites.to_sql(name='aqs', con=db, index=False)
pa_sites.to_sql(name='pa', con=db, index=False)
query = f'''
SELECT
aqs.site_id AS aqs_id,
pa.id AS pa_id,
pa.label AS pa_label,
aqs.lat AS aqs_lat,
aqs.lon AS aqs_lon,
pa.lat AS pa_lat,
pa.lon AS pa_lon
FROM aqs JOIN pa
ON  pa.lat - {offset_in_lat} <= aqs.lat
AND                             aqs.lat <= pa.lat + {offset_in_lat}
AND pa.lon - {offset_in_lon} <= aqs.lon
AND                             aqs.lon <= pa.lon + {offset_in_lon}
'''
matched = pd.read_sql(query, db)
matched
aqs_id
pa_id
pa_label
aqs_lat
aqs_lon
pa_lat
pa_lon
0
06-019-0011
6568
IMPROVE_FRES2
36.79
-119.77
36.79
-119.77
1
06-019-0011
13485
AMTS_Fresno
36.79
-119.77
36.79
-119.77
2
06-019-0011
44427
Fresno CARB CCAC
36.79
-119.77
36.79
-119.77
...
...
...
...
...
...
...
...
146
53-061-1007
3659
Marysville 7th
48.05
-122.17
48.05
-122.17
147
53-063-0021
54603
Augusta 1 SRCAA
47.67
-117.36
47.67
-117.36
148
56-021-0100
50045
WDEQ-AQD Cheyenne NCore
41.18
-104.78
41.18
-104.78
149 rows × 7 columns
We’ve achieved our goal—we matched 149 AQS sites with PurpleAir sensors.
Our wrangling of the locations is complete, and we turn to the task of
wrangling and cleaning the sensor measurements. We start with the measurements taken from an AQS site.
1
This estimation works by assuming that the Earth is perfectly spherical.
Then, one degree of latitude is the
radius of the Earth in meters.
Plugging in the average radius of the Earth gives 111,111 meters per degree of latitude.
Longitude is the same, but the radius of each “ring” around the Earth decreases
as we get closer to the poles, so we adjust by a factor of \( \cos(\text{lat}) \) .
It turns out that the Earth isn’t perfectly spherical, so these estimations
can’t be used for precise calculations, like landing a rocket.
But for our purposes, they do just fine.
