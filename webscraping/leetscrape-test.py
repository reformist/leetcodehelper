from leetscrape import GetQuestionsList
import requests

# building my own leetscrape because their's gives an error
# because leetcode knows it's coming from a script rather than browser

'''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get("https://leetcode.com/api/problems/all/", headers=headers)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code}, {response.text}")

print(response.text)

'''

'''
ls = GetQuestionsList()
ls.scrape() # Scrape the list of questions
ls.questions.head() # Get the list of questions
'''

# Creating a session object
session = requests.Session()

# Setting default headers for all requests made through this session
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# If needed, you can also set proxies, auth, verify, etc.
# session.proxies.update(...)
# session.auth = (username, password)
# session.verify = '/path/to/certfile'

# Making a request using the session
response = session.get('https://leetcode.com/api/problems/all/')

# When you're done with the session, you can close it to free up resources
session.close()

print(response.text)