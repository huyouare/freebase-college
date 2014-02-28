import csv
import json
import urllib
import sys
import re
# import us
# from bs4 import BeautifulSoup

#TODO: Add state support without dragging confidence down

states = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}


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
  college = College(upstart_id, name, sat_score, graduatation_rate, retention_rate)
  return college

collegeList = []

def read_file(f):
  with open(f, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    for row in reader:

      # college_name = row[1].replace('--', ' ')
      college_name = row[1]
      regex = re.compile(r'\b(' + '|'.join(states) + r')\b')
      abbr = regex.search(college_name)
      if abbr:
        abbr = abbr.group(0)
        print(abbr)
        college_name = college_name.replace(abbr, states[abbr])
        print(college_name)
      newCollege = College(row[0], college_name, (row[2] if len(row)>2 else None), (row[3] if len(row)>3 else None), (row[4] if len(row)>4 else None))
      collegeList.append(newCollege)

  print(College.collegeCount)

def process_reconcile(college):
  with open('reconcile.tsv', 'a') as rec:
    w = csv.writer(rec, delimiter = '\t')
    w.writerow([college.upstart_id] + [college.name] + [college.sat_score] + [college.retention_rate] + [college.graduatation_rate])
  params = {
    'name': college.name,
    'kind': '/education/university',
    # 'prop': ["/location/location/containedby:" + college.city, " /location/location/containedby:" + college.state],
    'key': api_key
  }
  reconcile(college, params)



def reconcile(college, params):

  service_url = 'https://www.googleapis.com/freebase/v1/reconcile'   

  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  with open('error.log', 'a') as f: # Simple logging, only for reconciliation
    if response is None:
      f.write("ERROR NO RESPONSE")
      return
    if 'match' in response.keys():
      f.write("Match: " + response['match'])
      college.freebase_id = response['match']['mid']
      college.result_name = response['match']['name'].encode('utf-8')
      college.confidence = response['match']['confidence']
    elif 'candidate' in response.keys():
      college.freebase_id = response['candidate'][0]['mid']
      college.result_name = response['candidate'][0]['name'].encode('utf-8')
      college.confidence = response['candidate'][0]['confidence']
      for candidate in response['candidate']:
        print(candidate['mid'] + ' (' + str(candidate['confidence']) + ')')
    else:
      college.result_name = None
      # f.write("No candidates for: " + college.name)

def search_all():
  service_url = 'https://www.googleapis.com/freebase/v1/search'  
  for college in collegeList:
    params = {
      'query': college.name,
      'type': '/education/university', 
      'key': api_key
    }

    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    if len(response['result'])==0:
      print("Reconciling: " + college.name)
      process_reconcile(college)
    elif response['result'][0]['score']<200:
      print("Score is: " + str(response['result'][0]['score']))
      process_reconcile(college)
    else:
      college.freebase_id = response['result'][0]['mid']
      college.result_name = response['result'][0]['name'].encode('utf-8')
      college.score = response['result'][0]['score']
    
def write_file():
  with open('output.tsv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["u_id"] + ["f_id"] + ["score"] + ["actual name"] + ["result name"])
    for college in collegeList:
      if college.score:
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.score] + [college.name] + [college.result_name])
      elif college.confidence:
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence] + [college.name] + [college.result_name])
      else:
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence] + [college.name] + "No result")
# if college.name != college.result_name:
    # print(college.name + " VS \n" + college.result_name);

if __name__ == '__main__':
  api_key = open(".freebase_api_key").read()
  # college = College(1, "Rutgers the State University of New Jersey Newark", 0, 0, 0)
  # reconcile(college)
  if len(sys.argv)==1: # if no arguments, use random Wikipedia page
    input_file = "colleges_for_jesse.tsv"
  else:
    input_file = sys.argv[1]
  read_file(input_file)
  search_all()
  write_file()