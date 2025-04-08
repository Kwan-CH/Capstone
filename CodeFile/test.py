import requests

response = requests.get('https://jian.sh/malaysia-api/state/v1/all.json')
all_data = response.json()
# print(selangor_data.get('administrative_districts'))
for data in all_data:
    state = data.get('state').replace(' ', '_').lower()
    state_data = requests.get(f'https://jian.sh/malaysia-api/state/v1/{state}.json')
    data = state_data.json().get('administrative_districts')
    print(data)

## Hi testing 
# ababaabbababa
word = 'hello world'
print(word)