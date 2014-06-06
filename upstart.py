import csv
import json
import urllib
import sys
import re
import math

states = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming' }

collegeList = []

class College(object):
  collegeCount = 0

  def __init__(self, upstart_id, name, sat_score, graduatation_rate, retention_rate):
    self.upstart_id = upstart_id
    self.name = name
    self.sat_score = sat_score
    self.graduatation_rate = graduatation_rate
    self.retention_rate = retention_rate
    self.freebase_id = None
    self.result_name = None;
    self.confidence = None
    self.score = None
    College.collegeCount += 1

def make_college(upstart_id, name, sat_score, graduatation_rate, retention_rate):
  """Constructor for College objects"""
  college = College(upstart_id, name, sat_score, graduatation_rate, retention_rate)
  return college

def read_file(input_file):
  """Generate College objects from input tsv, appending into collegeList
  Argument:
  input_file -- name of .tsv to be read
  """
  with open(input_file, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    for row in reader:
      newCollege = College(row[0], row[1], (row[2] if len(row)>2 else None), (row[3] if len(row)>3 else None), (row[4] if len(row)>4 else None))
      collegeList.append(newCollege)

  print(College.collegeCount)

def process_reconcile(college):
  """Additional reconciliation for a single college.
  Called when initial Search returns no results.
  Returns True if reconciliation successful, False if no results found.
  """
  with open('reconcile-schema.tsv', 'a') as rec:
    w = csv.writer(rec, delimiter = '\t')
    w.writerow([college.upstart_id] + [college.name] + [college.sat_score] + [college.retention_rate] + [college.graduatation_rate])
  
  # Try removing dashes and replacing abbreviation
  college_name = college.name.replace('--', ' ')
  regex = re.compile(r'\b(' + '|'.join(states) + r')\b')  # find all instances of state abbreviations
  abbr = regex.search(college_name)
  if abbr:  # If abbreviation found, replace with full name
    abbr = abbr.group(0)
    print("Abbreviation: " + abbr)
    college_name = college_name.replace(abbr, states[abbr])
  print(college_name)

  params = {
    'query': college_name,
    'type': '/education/university', 
    'key': api_key
  }
  rec_params = { # Parameters for Reconciliation API differ from Search API
    'name': college_name,
    'kind': '/education/university',
    # 'prop': ["/location/location/containedby:" + college.city, " /location/location/containedby:" + college.state],
    'key': api_key
  }

  if abbr: # If name did contain state abbreviation, search again
    if(search(college, params)):
      return True
    if(reconcile(college, rec_params)):
      return True
    # Then try omitting abbreviations and double-dash entirely
    college_name = college.name.replace('--', ' ')
    regex = re.compile(r'\b(' + '|'.join(states) + r')\b')
    abbr = regex.search(college_name)
    abbr = abbr.group(0)
    college_name = college_name.replace(abbr, ' ')
    params['query'] = college_name
    params['name'] = college_name
    if(search(college, params)):
      return True
    if(reconcile(college, rec_params)):
      return True

  # Finally, we try just the university name without campus/city
  college_name = college.name.split('--', 1)[0]
  college_name = college_name.split('-', 1)[0]
  params['query'] = college_name
  rec_params['name'] = college.name
  print(college_name)
  if(search(college, params)):
    print(college.result_name)
    college.score = 10 # Mark confidence as very low
    return True
  if(reconcile(college, rec_params)):
    print(college.result_name)
    college.score = 10
    return True

  return False
      
def search(college, params):
  """Calls Freebase Search API for a single college, given params
  Returns True if result found, False otherwise
  """
  service_url = 'https://www.googleapis.com/freebase/v1/search'
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  if response['result']:
    college.freebase_id = response['result'][0]['mid']
    college.result_name = response['result'][0]['name'].encode('utf-8')
    college.score = response['result'][0]['score']
    return True
  else:
    return False


def reconcile(college, params):
  """Calls Freebase Reconciliation API for a single college, given params
  Returns True if result found, False otherwise
  """
  service_url = 'https://www.googleapis.com/freebase/v1/reconcile'   
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  if response is None:
    return False
  if 'match' in response.keys():
    college.freebase_id = response['match']['mid']
    college.result_name = response['match']['name'].encode('utf-8')
    college.confidence = response['match']['confidence']
    return True
  if 'candidate' in response.keys():
    college.freebase_id = response['candidate'][0]['mid']
    college.result_name = response['candidate'][0]['name'].encode('utf-8')
    college.confidence = response['candidate'][0]['confidence']
    for candidate in response['candidate']:
      print(candidate['mid'] + ' (' + str(candidate['confidence']) + ')')
    return True
  else:
    college.result_name = None
    return False

def search_all():
  """Conducts search on all Colleges in collegeList using Freebase Search API.
  Writes intermediate results to output-debut.tsv.
  """
  service_url = 'https://www.googleapis.com/freebase/v1/search'
  with open('output-debug-schema.tsv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["u_id"] + ["f_id"] + ["score"] + ["actual name"] + ["result name"])  
    
    for college in collegeList:
      params = {
        'query': college.name,
        'type': '/education/university', 
        'scoring': 'schema'
      }
      url = service_url + '?' + urllib.urlencode(params)
      response = json.loads(urllib.urlopen(url).read())

      if response['status'] != "200 OK":
        print(response['status'])
      elif len(response['result'])==0:  # If no result found, additional processing performed.
        print("Reconciling: " + college.name)
        process_reconcile(college)

      # elif response['result'][0]['score']<200:
        # print("Score is: " + str(response['result'][0]['score']))
      #   process_reconcile(college)

      else: # Store result's Freebase ID, college name, and score
        college.freebase_id = response['result'][0]['mid']
        college.result_name = response['result'][0]['name'].encode('utf-8')
        college.score = response['result'][0]['score']
    
      # if college.name != college.result_name:
          # print(college.name + " VS \n" + college.result_name);

      if college.score:
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.score] + [college.name] + [college.result_name])
      elif college.confidence: # Reconciliation API's built-in confidence
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence] + [college.name] + [college.result_name])
      else:
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence] + [college.name] + ["No result"])

      if college.score<=1:
        college.confidence = 0.00
      elif college.score>=3000: # few with over 3000
        college.confidence = 100.00
      else:
        college.confidence = round(math.log(college.score, 3000)*100, 2)
      
def write_file():
  """Write final results of all Colleges to output.tsv
  """
  with open('output-schema.tsv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["upstart_id"] + ["freebase_id"] + ["confidence"])  
    for college in collegeList:
      writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence])

if __name__ == '__main__':
  api_key = open(".freebase_api_key").read()
  open('reconcile-schema.tsv', 'w').close()  # remove contents of reconcile.tsv
  if len(sys.argv)==1:  # if no arguments, use default .tsv file
    input_file = "colleges_for_jesse.tsv"
  else:
    input_file = sys.argv[1]
  read_file(input_file)
  search_all()
  write_file()