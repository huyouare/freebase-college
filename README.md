Upstart & Freebase College Reconciliation
=========================================

Goal:

###Notes:
* ".encode('utf-8')" necessary for strings with particular characters.
* Input file contains "--" when appending city or campus name to university name ("University of State--Campus"). The college name in the Freebase result usually appears as "University of State Campus", "University of State, Campus" or "University of State at Campus".
* Initially the Reconciliation endpoint of the Freebase API was considered for use to target those that could not be found via Search. However, results were not produced.
* Instead, variations of the college name were needed for Freebase to find the correct Freebase ID.

###Procedure:
* Regular Search was used to find Freebase IDs by provided college names. Checking manually for results, this produced most of the data. The 'score' provided by Freebase Search and the difference in strings (difflib) determines whether or not to further reconcile
* Rutgers, the State University of New Jersey--Newark:
Freebase Search could not provide results for "Rutgers the State University of New Jersey Newark". "Rutgers, the State University of New Jersey" returns Rutgers University (/m/0ks67). "Rutgers Newark" provides Rutgers-Newark (/m/074p0t).
* Aquinas College - Grand Rapids, MI:
Aquinas College - Nashville, TN
etc.
Freebase search did not produce results. Correct results came from "Aquinas College Grand Rapids". Freebase Search does not cooperate with two-letter state abbreviations in search query.
http://code.activestate.com/recipes/577305-python-dictionary-of-us-states-and-territories/
http://stackoverflow.com/questions/2313032/regex-for-state-abbreviations-python

Berkeley College - Woodland Park, NJ
Berkeley College - New York, NY 

Bethel College - Mishawaka, IN
Sometimes results appear with abbreviations rather than full state name (IN over Indiana). We must try both.

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