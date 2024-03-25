import requests
import json

# The GraphQL endpoint URL
url = 'https://leetcode.com/graphql'

# The query to fetch question details by its titleSlug
query = """
query questionTitle($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    isPaidOnly
    difficulty
    likes
    dislikes
  }
}
"""

# Variable to be replaced in the query
variables = {"titleSlug": "two-sum"}

# Headers may need to include additional items such as 'Content-Type' and potentially 'Authorization' for APIs that require authentication
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"  # Mimicking a browser's User-Agent to avoid potential blocking
}

# Making a POST request to the GraphQL endpoint with the query and variables
response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

# Parsing the response data to JSON
data = response.json()

# Printing out the data
print(json.dumps(data, indent=2))
