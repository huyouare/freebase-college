import csv
import json
import urllib

#TODO: Add state support without dragging confidence down

class College(object):
    collegeCount = 0

    def __init__(self, name, upstart_id, city, state):
        self.name = name
        self.upstart_id = upstart_id
        self.city = city
        self.state = state
        self.freebase_id = None
        self.confidence = 0
        College.collegeCount += 1

def make_college(name, upstart_id, city, state):
    college = College(name, upstart_id, city, state)
    return college

collegeList = []

with open('input.csv', 'rb') as f:
  reader = csv.reader(f)
  for row in reader:
    print row
    newCollege = College(row[1], row[0], row[2], row[3])
    # for i, col in enumerate(row):
    collegeList.append(newCollege)

print(College.collegeCount)

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/reconcile'   
for college in collegeList:
  params = {
    'name': 'college',
    'kind': '/education/university',
    'prop': ["/location/location/containedby:" + college.city, " /location/location/containedby:" + college.state],
    'key': api_key
  }
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  # if 'match' in response:
  #   print response['match']
  #   college.confidence = response['match'].confidence
  if response['candidate'] is None:
    print("ERROR NO CANDIDATE")
    continue
  college.freebase_id = response['candidate'][0]['mid']
  college.confidence = response['candidate'][0]['confidence']
  for candidate in response['candidate']:
    print candidate['mid'] + ' (' + str(candidate['confidence']) + ')'

service_url = 'https://www.googleapis.com/freebase/v1/search'
for college in collegeList:
  query = college.name
  params = {
    'query': "college",
    'type': '/education/university', 
    'filter': "(all type:/education/university " + \
      "/location/location/containedby:\"" + college.city + "\" " + \
      "/location/location/containedby:\"" + college.state + "\""+ ")",
    'key': api_key
  }
  print(params)
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  for result in response['result']:
    print result['mid'] + ' (' + str(result['score']) + ')'
  college.freebase_id = response['result'][0]['mid']
  college.confidence = response['result'][0]['score']


with open('output.csv', 'wb') as f:
  writer = csv.writer(f, delimiter=',')
  for college in collegeList:
    writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence])