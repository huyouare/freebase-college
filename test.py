import json
import urllib

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/reconcile'
params = {
        'name': 'Yale University',
        'kind': '/education/university',
        #'prop': '/film/film/directed_by:Ridley Scott',
        'key': api_key
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
if 'match' in response:
  print response['match']
for candidate in response['candidate']:
    print candidate['mid'] + ' (' + str(candidate['confidence']) + ')'