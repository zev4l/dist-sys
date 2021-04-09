import requests
import json

# Check reference client on how to use requests module to query the REST server

# For argument checking and all the rest, rip it from the v2 client


#### TEST LINES - PROOF OF CONCEPT

# utilizador = {'nome': "João Café", 'senha': "AAAAAAAAAAAAA"}
# r = requests.post('http://localhost:5000/utilizadores', json = utilizador)
# print(r.status_code)
# print('***')

####
#
r = requests.delete('http://localhost:5000/utilizadores')
print(r.status_code)
print('***')

####

# r = requests.get('http://localhost:5000/utilizadores')
# print(r.status_code)
# print('***')

####

# utilizador = {'senha': 'TESTE123123123'}
# r = requests.put('http://localhost:5000/utilizadores/5', json = utilizador)
# print(r.status_code)
# print('***')
