import requests


url = "https://api.countrystatecity.in/v1/countries/MY/states"

headers = {
  'X-CSCAPI-KEY': 'S1FOTHE5OW56bXpRWDNVQmpwckhZMFliYXgyNU9nUkZKRm1DRlc5bA=='
}

response = requests.request("GET", url, headers=headers).json()

state_code = []
for data in response:
    state_code.append(data.get('iso2'))
    print(data.get('name'), data.get('iso2'))

for state_city in state_code:
    if state_city=='14':
        print('\n\n')
        url = f"https://api.countrystatecity.in/v1/countries/MY/states/{state_city}/cities"
        response = requests.request("GET", url, headers=headers).json()
        for data in response:
            print(data)
    # for area in response:
    #     print(area.get('name'))