import csv
import json
import urllib

# api_key = open(".freebase_api_key").read()
infile = open('output-debug-schema-with-ratios-and-comments.csv', 'rbU')
reader = csv.reader(infile)

with open('output-debug-schema-with-ipeds-and-comments.csv', 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(["u_id"] + ["f_id"] + ["ipeds_id"] + ["score"] + ["actual name"] + ["result name"])  
  
  next(reader)
  for row in reader:
    freebase_id = row[1]

    api_key = "AIzaSyB__vvvcbdwU5ohhONFfcouu-AwYK3kBGU"
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    if freebase_id and freebase_id != "":
      query = [{
        "id": freebase_id,
        "key": [{
          "namespace": "/authority/nces/ipeds",
          "value": None,
          "limit": 1
        }]
      }]
      params = {
              'query': json.dumps(query),
              'key': api_key
      }
      url = service_url + '?' + urllib.urlencode(params)
      response = json.loads(urllib.urlopen(url).read())

      if 'result' not in response.keys():
        print response
        writer.writerow([row[0], row[1], "", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
      else:
        if len(response['result']) == 0:
          ipeds = ""
        else: 
          ipeds = response['result'][0]['key'][0]['value']
        writer.writerow([row[0], row[1], ipeds, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])

    else:
      writer.writerow([row[0], row[1], "", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
