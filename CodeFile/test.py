# import requests
#
#
# url = "https://api.countrystatecity.in/v1/countries/MY/states"
#
# headers = {
#   'X-CSCAPI-KEY': 'S1FOTHE5OW56bXpRWDNVQmpwckhZMFliYXgyNU9nUkZKRm1DRlc5bA=='
# }
#
# response = requests.request("GET", url, headers=headers).json()
#
# state_code = []
# for data in response:
#     state_code.append(data.get('iso2'))
#     print(data.get('name'), data.get('iso2'))
#
# for state_city in state_code:
#     if state_city=='14':
#         print('\n\n')
#         url = f"https://api.countrystatecity.in/v1/countries/MY/states/{state_city}/cities"
#         response = requests.request("GET", url, headers=headers).json()
#         for data in response:
#             print(data)
#     # for area in response:
#     #     print(area.get('name'))

import os
from pathlib import Path

def print_tree(startpath, level=0):
    for item in sorted(os.listdir(startpath)):
        path = os.path.join(startpath, item)


        if item.startswith('.') or item == 'myenv' or item == '__pycache__':
            continue

        if os.path.isdir(path):
            print('│   ' * level + '├── ' + item)
            print_tree(path, level + 1)
        else:
            if level == 0:  # ✅ Only print files in the top-level directory
                print('│   ' * level + '├── ' + item)

# path = Path(__file__).parents[0]
# print(path)
path = Path(__file__).parents[1]
print(path)
print_tree(path)


#
# p = Path(__file__).parents[1]
#
# print(p.joinpath(os.getcwd()))
#
# import os.path as path
#
# two_up =  path.abspath(path.join(__file__ ,"../..", os.getcwd()))
#
# print(two_up)