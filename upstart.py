import csv
import json
import urllib

class College(object):
    collegeCount = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, upstart_id, city):
        self.name = name
        self.upstart_id = upstart_id
        self.city = city
        self.freebase_id = None
        self.confidence = 0
        College.collegeCount += 1

def make_college(name, upstart_id, city):
    college = College(name, upstart_id, city)
    return college

collegeList = []


with open('input.csv', 'rb') as f:
  reader = csv.reader(f)
  for row in reader:
    print row
    newCollege = College(row[1], row[0], row[2])
    # for i, col in enumerate(row):
    collegeList.append(newCollege)

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/reconcile'   
for college in collegeList:
  params = {
          'name': college.name,
          'kind': '/education/university',
          'prop': '/location/location/containedby:' + college.city,
          'key': api_key
  }
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())
  if 'match' in response:
    print response['match']
  for candidate in response['candidate']:
      print candidate['mid'] + ' (' + str(candidate['confidence']) + ')'