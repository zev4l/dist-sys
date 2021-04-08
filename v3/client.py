import requests
import json

# Check reference client on how to use requests module to query the REST server

# For argument checking and all the rest, rip it from the v2 client


#### TEST LINES - PROOF OF CONCEPT

r = requests.get('http://localhost:5000/utilizadores')
print(r.status_code)
print(r.json())
print(r.headers)
print('***')

####
