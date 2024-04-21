from __future__ import print_function

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import os

from openai import OpenAI
import openai

import traceback
import re

import os.path
import sys

import base64

# import statements
from leetscrape import GetQuestionsList, GetQuestion, GenerateCodeStub, ExtractSolutions
from bs4 import BeautifulSoup

import requests
import json

# test change

load_dotenv(find_dotenv())
app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5000", "http://localhost:3000"]}}) # same port number
CORS(app, resources={r"/*": {"origins": "*"}})


# constant variables

# The GraphQL endpoint URL
url = 'https://leetcode.com/graphql'

'''
Test method
'''
@app.route('/', methods = ["GET"])
def root():
    return {
        'test': True,
    }

@app.route('/test', methods=["GET"]) # GET request, with input params
def test(): # when user submits a request to add event to calendar
    return {
        'success': True,
    }

'''
Route to submit problem name, starting code

Return the hints for the user
'''
@app.route('/hints', methods=["GET", "POST"]) # GET request, with input params
def get_hints(): # when user submits a request to add event to calendar
    # Retrieve 'problem_name' from query parameters
    problem_name = request.args.get('problem_name', '')
    problem_description = get_problem_description(problem_name)
    # problem_code = get_problem_code(problem_name)
    problem_code = request.args.get('problem_code', '')

    print(" ------------ PROBLEM DESCRIPTION ------------ ")
    print(problem_description)

    print(" ------------ PROBLEM CODE ------------ ")
    print(problem_code)

    # Generate a response using GPT

    messages = [] # list of messages for gpt
    # in messages, we want the first item to be the system response

    # before adding any messages, set the instructions
    instructions = define_instructions()
    messages.append({'role': 'system', 'content': instructions})
    
    # user message
    message = f'''
    Provide me with hints for this problem:

    Problem Description:

    {problem_description}

    Starting Code:

    {problem_code}
    '''

    message = {'role': 'user', 'content': message} # roles - user, assistant
    messages.append(message)

    # generate new response from gpt
    new_messages = generate(messages)
    response = new_messages[-1]['content'].strip() # take the last (most recent) message

    try:
        return {
            'success': True,
            'response': response
        }
    except Exception as e:
        # printing stack trace of error
        traceback.print_exc()

        return {
            'success': False,
            'error': str(e)
        }, 500

'''
Helper method for obtaining the problem description based on name
'''
def get_problem_description(name):
    # The query to fetch question content by its titleSlug
    query = """
    query questionContent($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        content
        mysqlSchemas
    }
    }
    """

    # Variable to be replaced in the query
    variables = {"titleSlug": name}

    # Headers may need to include additional items such as 'Content-Type' and potentially 'Authorization' for APIs that require authentication
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # Mimicking a browser's User-Agent to avoid potential blocking
    }

    # Making a POST request to the GraphQL endpoint with the query and variables
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # proceed with your data processing
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

    # Parsing the response data to JSON
    data = response.json()

    print(data)

    # Extracting the problem content (description) with HTML
    problem_content_html = data['data']['question']['content']

    # Using BeautifulSoup to parse HTML and extract text
    soup = BeautifulSoup(problem_content_html, 'html.parser')
    problem_content_text = soup.get_text()

    # Printing the clean text content
    return problem_content_text

'''
Helper method for obtaining the problem starter code
'''
def get_problem_code(name):
    # The query to fetch code snippets by its titleSlug
    query = """
    query questionEditorData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        codeSnippets {
        lang
        langSlug
        code
        }
        envInfo
        enableRunCode
    }
    }
    """

    # Variable to be replaced in the query
    variables = {"titleSlug": name}

    # Headers may need to include additional items such as 'Content-Type'
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # Mimicking a browser's User-Agent to avoid potential blocking
    }

    # Making a POST request to the GraphQL endpoint with the query and variables
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # proceed with your data processing
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

    # Parsing the response data to JSON
    data = response.json()

    # Extracting code snippets
    code_snippets = data['data']['question']['codeSnippets']

    # Filter the code snippets for a specific language, e.g., Python
    python_snippet = next((snippet for snippet in code_snippets if snippet['langSlug'] == 'python'), None)

    if python_snippet:
        return python_snippet['code']
    else:
        return None

'''
Initial instructions for GPT
'''
def define_instructions():

    output = {
	    "hints": "Let's first break down the known parameters. We have two lists (nums1, nums2) and two numbers (m, n) indicating the size of those lists. How can we use this information to iterate over the elements?"
    }

    output = json.dumps(output) # convert to JSON-readable string
    
    instructions = f'''
    Here are instructions for each of my subsequent queries. 
    
    You will provide hints on how to tackle a particular coding problem. Return a JSON response. Here is an example of an input, output pair:

    Input:

    Problem Description:

    You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

    Merge nums1 and nums2 into a single array sorted in non-decreasing order.

    The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

    Starting Code:

    class Solution(object):
        def merge(self, nums1, m, nums2, n):
            """
            :type nums1: List[int]
            :type m: int
            :type nums2: List[int]
            :type n: int
            :rtype: None Do not return anything, modify nums1 in-place instead.
            """

    Output:

    {output}

    Make sure to provide general hints to guide the user, DO NOT just give away the solution.
    
    Finally, make your hints as concise as possible (2-3 short sentences or less).
    '''

    # for now, make it succint
    # later want to separate hints into numbers

    return instructions

'''
Generate a new response using GPT
'''
'''
New method using gpt-4 turbo and JSON mode
'''
def generate(MESSAGES):

    # OPEN AI SETUP - NEW
    api_key = os.getenv('OPENAI_API_KEY')
    # openai.api_key = api_key

    client = OpenAI(
        api_key=api_key
    )

    MODEL = 'gpt-3.5-turbo-1106'
    # MODEL = 'gpt-4-turbo-preview' # UPGRADING TO GPT 4, can use the turbo version later on
    # model = 'gpt-3.5-turbo' # can try with gpt 4 later

    try:
        response = client.chat.completions.create(
        model=MODEL,
        response_format={ "type": "json_object" },
        messages=MESSAGES
        )

        MESSAGES.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")

    return MESSAGES

if __name__ == '__main__':
   app.run(port=8001, debug=True)