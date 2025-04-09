import requests

def getState():
    url = "https://api.countrystatecity.in/v1/countries/MY/states"

    headers = {
        'X-CSCAPI-KEY': 'S1FOTHE5OW56bXpRWDNVQmpwckhZMFliYXgyNU9nUkZKRm1DRlc5bA=='
    }

    response = requests.request("GET", url, headers=headers).json()

    states = {}

    for state in response:
        states[state.get('name')] = state.get('iso2')

    return states