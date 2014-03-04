Upstart & Freebase College Reconciliation
=========================================

###Goal:
Take existing colleges and reconcile them to Google's Freebase.com database. 

####Input:
A spreadsheet of school information as a TSV. Format:

`Upstart ID,  Name,  Median SAT score,  Graduation rate, Retention rate`

####Output:
Output as a TSV with the following format:

`Upstart ID*, Freebase ID, Confidence %`

This file should contain all of the schools we gave you in the initial file, and an English (not code) explanation of the methodology you used to generate the Confidence %. (*Upstart ID is just an arbitrary number we assign to schools, to give them a unique ID in our database.)

####Notes:
* ".encode('utf-8')" necessary for strings with non-English characters.
* Input file contains "--" when appending city or campus name to university name ("University of State--Campus"). The college name in the Freebase result usually appears as "University of State Campus", "University of State, Campus" or "University of State at Campus".
* Changed state abbreviations to full names. 
http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/

###Procedure:
* The Search API was used to find Freebase IDs by provided college names. Checking manually for results, this produced most of the data. The 'score' is provided by Freebase Search and 
* The difference in strings (difflib) determines whether or not to further reconcile
* Initially the Reconciliation endpoint of the Freebase API was considered for use to target those that could not be found via Search. However, results were not produced for all colleges provided.
* Instead, variations of the college name are needed for Freebase to find the correct Freebase ID.

####Corner Cases:
* Rutgers, the State University of New Jersey--Newark:
Freebase Search could not provide results for "Rutgers the State University of New Jersey Newark". "Rutgers, the State University of New Jersey" returns Rutgers University (/m/0ks67). "Rutgers Newark" provides Rutgers-Newark (/m/074p0t).
* Berkeley College - Woodland Park, NJ did not exist.
* Bethel College - Mishawaka, IN
Sometimes results appear with abbreviations rather than full state name (IN over Indiana). We must try both.
* Emmanuel College - Franklin Springs, Georgia
Works with "Emmanuel College Georgia" but cannot include "Franklin Springs"
* Union College - Barbourville, Kentucky and Union College - Schenectady, New York don't allow abbreviation "KY", though Union College - Lincoln, Nebraska does.
* Very few abbreviated universities. These seem to be correct:
JMU -> James Madison University
Derby -> University of Derby


### Getting Started
######Install dependencies:  
`pip install -r requirements.txt`

###### Using the script:  
`python upstart.py TSV_FILE`

###### Example:  
`python upstart.py colleges_for_jesse.tsv`

###### Sample Output:  
```
upstart_id freebase_id confidence
1 /m/02rk23 0.811214889875
2 /m/01t8sr 0.841746194072
3 /m/03818y 0.808804657761
4 /m/02ldkf 0.808932328004
5 /m/02hdht 0.7583775629631
```

###### Testing (100 random trials):  
`python test.py`