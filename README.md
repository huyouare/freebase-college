Upstart & Freebase College Reconciliation
=========================================

###Goal
Write some code (an app, a script, etc.) that takes existing colleges and reconciles them to Google's Freebase.com database. Use whatever technologies and heuristics you can to make this as comprehensive and accurate as possible.

####Input
A spreadsheet of school information as a CSV or TSV. Format: 
ID  Name  Median SAT score  Graduation rate Retention rate

####Output
Your code, along with its output as a CSV or TSV with the following format:
Upstart ID*, Freebase ID, Confidence %

This file should contain all of the schools we gave you in the initial file, and an English (not code) explanation of the methodology you used to generate the Confidence %. (*Upstart ID is just an arbitrary number we assign to schools, to give them a unique ID in our database.)

###Notes:
* ".encode('utf-8')" necessary for strings with particular characters.
* Input file contains "--" when appending city or campus name to university name ("University of State--Campus"). The college name in the Freebase result usually appears as "University of State Campus", "University of State, Campus" or "University of State at Campus".
* Changed state abbreviations to full names
http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
http://stackoverflow.com/questions/2313032/regex-for-state-abbreviations-python

###Procedure:
* The Search API was used to find Freebase IDs by provided college names. Checking manually for results, this produced most of the data. The 'score' provided by Freebase Search and the difference in strings (difflib) determines whether or not to further reconcile
* Initially the Reconciliation endpoint of the Freebase API was considered for use to target those that could not be found via Search. However, results were not produced for all colleges provided.
* Instead, variations of the college name were needed for Freebase to find the correct Freebase ID.

####Corner Cases:
* Rutgers, the State University of New Jersey--Newark:
Freebase Search could not provide results for "Rutgers the State University of New Jersey Newark". "Rutgers, the State University of New Jersey" returns Rutgers University (/m/0ks67). "Rutgers Newark" provides Rutgers-Newark (/m/074p0t).

Berkeley College - Woodland Park, NJ
Berkeley College - New York, NY 

Bethel College - Mishawaka, IN
Sometimes results appear with abbreviations rather than full state name (IN over Indiana). We must try both.

Emmanuel College - Franklin Springs, Georgia  No result found for Emmanuel College - Franklin Springs, Georgia

1623  /m/035g_2 130.999451  Union College - Barbourville, Kentucky  Union College
1624  /m/035h0h 148.6492  Union College - Lincoln, Nebraska Union College
1625  /m/02ccqg 387.929993  Union College - Schenectady, New York Union College

633 /m/048nry 131.263626  Aquinas College - Grand Rapids, Michigan  Aquinas College
634 /m/066pm6 79.031181 Aquinas College - Nashville, Tennessee  Aquinas College

2004  /m/0438f  18.477449 JMU James Madison University

2017  /m/0344bc 42.02314  Derby University of Derby


### Getting Started
######Install dependencies:  
`pip install -r requirements.txt`

###### Using the script:  
`python upstart.py TSV_FILE`

###### Example:  
`python upstart.py colleges_for_jesse.tsv`

###### Output:  


###### Testing (100 random trials):  
`python test.py`