import csv
import json
import urllib
import sys
# import requests, re
# from bs4 import BeautifulSoup

#TODO: Add state support without dragging confidence down

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
      print(row)
      newCollege = College(row[0], row[1], (row[2] if len(row)>2 else None), (row[3] if len(row)>3 else None), (row[4] if len(row)>4 else None))
      collegeList.append(newCollege)

  print(College.collegeCount)

def reconcile(college):
  service_url = 'https://www.googleapis.com/freebase/v1/reconcile'   
  params = {
    'name': college.name,
    'kind': '/education/university',
    # 'prop': ["/location/location/containedby:" + college.city, " /location/location/containedby:" + college.state],
    'key': api_key
  }
  url = service_url + '?' + urllib.urlencode(params)
  response = json.loads(urllib.urlopen(url).read())

  if 'match' in response:
    print(response['match'])
    college.freebase_id = response['match']['mid']
    college.result_name = response['match']['name']
    college.confidence = response['match']['confidence']
  if response['candidate'] is None:
    print("ERROR NO CANDIDATE")
  else:
    college.freebase_id = response['candidate'][0]['mid']
    college.confidence = response['candidate'][0]['confidence']
    for candidate in response['candidate']:
      print(candidate['mid'] + ' (' + str(candidate['confidence']) + ')')

def reconcile_all():
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
    if 'match' in response:
      print(response['match'])
      college.confidence = response['match'].confidence
    if response['candidate'] is None:
      print("ERROR NO CANDIDATE")
      continue
    college.freebase_id = response['candidate'][0]['mid']
    college.confidence = response['candidate'][0]['confidence']
    for candidate in response['candidate']:
      print(candidate['mid'] + ' (' + str(candidate['confidence']) + ')')

  with open('output.csv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    for college in collegeList:
      writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence])

def search():
  api_key = open(".freebase_api_key").read()

  service_url = 'https://www.googleapis.com/freebase/v1/search'
  for college in collegeList:
    params = {
      'query': college.name,
      'type': '/education/university', 
      # 'filter': "(all type:/education/university " + \


        # "/location/location/containedby:\"" + college.city + "\" " + \
        # "/location/location/containedby:\"" + college.state + "\""+ ")",
      'key': api_key
    }
    # print(params)
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    for result in response['result']:
      print(result['mid'] + ' (' + str(result['score']) + ')')
    college.freebase_id = response['result'][0]['mid']
    college.result_name = response['result'][0]['name']
    college.score = response['result'][0]['score']

  with open('output.csv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["u_id"] + ["f_id"] + ["score"] + ["actual name"] + ["result name"])
    for college in collegeList:
      writer.writerow([college.upstart_id] + [college.freebase_id] + [college.score] + [college.name] + [college.result_name])

def search_test():
  service_url = 'https://www.googleapis.com/freebase/v1/search'
  
  with open('output.tsv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["u_id"] + ["f_id"] + ["score"] + ["actual name"] + ["result name"])
     
    for college in collegeList:
      params = {
        'query': college.name,
        'type': '/education/university', 
        'key': api_key
      }

      url = service_url + '?' + urllib.urlencode(params)
      response = json.loads(urllib.urlopen(url).read())

      if len(response['result'])==0:
        print("Error: " + college.name)
        reconcile(college)
        writer.writerow([college.upstart_id] + [college.freebase_id] + [college.confidence] + [college.name] + [college.result_name])
        if college.name != college.result_name:
          print(college.name + " " + college.result_name);
      
      else:
        college.freebase_id = response['result'][0]['mid']
        college.result_name = response['result'][0]['name']
        college.score = response['result'][0]['score']
    
      writer.writerow([college.upstart_id] + [college.freebase_id] + [college.score] + [college.name] + [college.result_name])
      if college.name != college.result_name:
      	print(college.name + " " + college.result_name);

if __name__ == '__main__':
  api_key = open(".freebase_api_key").read()
  if len(sys.argv)==1: # if no arguments, use random Wikipedia page
    input_file = "college-sm.tsv"
  else:
    input_file = sys.argv[1]
  read_file(input_file)
  search_test()