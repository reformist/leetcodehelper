from __future__ import print_function

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import make_response

import os
import os.path
import sys

from openai import OpenAI
import openai

import traceback
import re

import base64
from bs4 import BeautifulSoup

import requests
import json

from supabase import create_client, Client

import pandas as pd

import pymongo
from pymongo import MongoClient

# test change

load_dotenv(find_dotenv())
app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5000", "http://localhost:3000"]}}) # same port number
CORS(app, resources={r"/*": {"origins": "*"}})

# constant variables

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')

TABLE_NAME = 'hints'

RATING_THRESHOLD = 0 # just needs to be greater than 0

openai.api_key = os.getenv('OPENAI_API_KEY')

EMBEDDING_MODEL = "text-embedding-3-small"

MONGO_PASSWORD = os.getenv('MONGO_PASS')

COSINE_THRESHOLD = 0.85 # a very close match was 0.94, bad was 0.75
# if above this, then "good match"
# otherwise, bad match

# The GraphQL endpoint URL
url = 'https://leetcode.com/graphql'

# constant variables

version = 1.1

# The GraphQL endpoint URL

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

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

    print("VERSION: " + str(version))

    # Retrieve 'problem_name' from query parameters

    print(request)

    problem_name = request.json.get('problem_name', '')
    problem_description = get_problem_description(problem_name)
    # problem_code = get_problem_code(problem_name)
    problem_code = request.json.get('problem_code', '')

    print(" ------------ PROBLEM DESCRIPTION ------------ ")
    print(problem_description)

    print(" ------------ PROBLEM CODE ------------ ")
    print(problem_code)

    # print(request.args)
    # print(request.args.get('problem_name'))

    # Generate a response using GPT

    messages = [] # list of messages for gpt
    # in messages, we want the first item to be the system response

    # print("DOES NOT BREAK HERE")

    # before adding any messages, set the instructions
    instructions = define_instructions()
    messages.append({'role': 'system', 'content': instructions})
    
    # user message
    message = f'''
    Provide me with a hint for this problem:

    Problem Description:
    {problem_description}

    Current Code:
    {problem_code}
    '''

    print("------msg that's fed to chatgpt")
    print(message)

    message = {'role': 'user', 'content': message} # roles - user, assistant
    messages.append(message)

    print("entire message sent to gpt")
    print(messages)

    # generate new response from gpt
    '''
    new_messages, source_info = generate(messages)
    # print(new_messages)
    response = new_messages[-1]['content'].strip() # take the last (most recent) message
    '''
    new_messages = generate(messages)
    # print(new_messages)
    response = new_messages[-1]['content'].strip() # take the last (most recent) message

    print(f"Response: {response}")
    # print(f"Source Information: \n{source_info}")

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
        "hint": "Let's first break down the known parameters. We have two lists (nums1, nums2) and two numbers (m, n) indicating the size of those lists. How can we use this information to iterate over the elements?"
    }

    output = json.dumps(output) # convert to JSON-readable string
    
    instructions = f'''
    You will provide a hint on how to tackle a Leetcode coding problem. The input is the problem name, description, and user's current code. The JSON output is your hint. 

    Make sure to provide a hint to guide the user, DO NOT just give away the solution. Consider what the user has coded so far (VERY IMPORTANT), and build advice on top of it. Finally, make your hints as concise as possible (2-3 short sentences or less).

    Here is an example:

    Problem Description:
    You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

    Merge nums1 and nums2 into a single array sorted in non-decreasing order.

    The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

    Current Code:
    class Solution(object):
        def merge(self, nums1, m, nums2, n):
            """
            :type nums1: List[int]
            :type m: int
            :type nums2: List[int]
            :type n: int
            :rtype: None Do not return anything, modify nums1 in-place instead.
            """

    Your Hint:
    {output}
    '''
    
    # for now, make it succint
    # later want to separate hints into numbers

    return instructions

'''
Generate a new response using GPT
'''
def generate(MESSAGES):

    # OPEN AI SETUP - NEW
    api_key = os.getenv('OPENAI_API_KEY')
    # openai.api_key = api_key

    client = OpenAI(
        api_key=api_key
    )

    # MODEL = 'gpt-3.5-turbo-1106'
    # MODEL = 'gpt-4-turbo'
    # MODEL = 'gpt-4-turbo-preview' # UPGRADING TO GPT 4, can use the turbo version later on
    # model = 'gpt-3.5-turbo' # can try with gpt 4 later
    MODEL = 'gpt-4o'

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={ "type": "json_object" }, # valid for gpt 4o
            messages=MESSAGES
        )

        MESSAGES.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")

    return MESSAGES

'''
Generate a new response using GPT
'''
def generate_old(MESSAGES):

    # OPEN AI SETUP - NEW
    api_key = os.getenv('OPENAI_API_KEY')
    # openai.api_key = api_key

    client = OpenAI(
        api_key=api_key
    )

    # MODEL = 'gpt-3.5-turbo-1106'
    # MODEL = 'gpt-4-turbo-preview' # UPGRADING TO GPT 4, can use the turbo version later on
    # model = 'gpt-3.5-turbo' # can try with gpt 4 later
    MODEL = "gpt-4o"

    query = MESSAGES[-1]['content'].strip() # most recent message is the user query

    _, collection = update_embeddings()

    get_knowledge = vector_search(query, collection)

    search_result = ''
    rating = 0

    for result in get_knowledge: # should just be one item
        search_result += f'''Problem: {result.get('problem_name', 'N/A')} \n\nCode: {result.get('code', 'N/A')} \n\nHint: {result.get('hint', 'N/A')} \n\n'''
        
        score = result.get('score', 'N/A')
        rating = result.get('rating', 'N/A')
        print("Search Score: " + str(score))

    # now check if the rating is above a certain threshold
    # if so, then add to the prompt

    if rating > RATING_THRESHOLD: # hint was liked by someone
        # now overwrite the query in the list
        MESSAGES[-1]['content'] += f'''\n\nPlease answer this user query with the following context: \n\n{search_result}
        '''

    print(f"New Query: \n{MESSAGES[-1]['content']}")

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=MESSAGES
        )

        MESSAGES.append({'role': completion.choices[0].message.role, 'content': completion.choices[0].message.content})

        # print("Assistant: " + completion.choices[0].message.content)
    
    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")

    return MESSAGES, search_result


'''
NEW METHODS
'''

# internal method
def get_embedding(text):
    """Generate an embedding for the given text using OpenAI's API."""

    # Check for valid input
    if not text or not isinstance(text, str):
        return None

    try:
        # Call OpenAI API to get the embedding
        embedding = openai.embeddings.create(input=text, model=EMBEDDING_MODEL).data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error in get_embedding: {e}")
        return None

# call this to set up database connections
# internal method
def update_embeddings():
    supabase: Client = create_client(url, key)

    # Fetch data from the table
    data = supabase.table("hints").select("*").execute()
    full_data = data.data
    # print(full_data)  # Outputs the fetched data

    supa_df = pd.DataFrame(full_data)

    # Now you can work with 'df' as a pandas DataFrame
    print(supa_df.head())

    # Database cleanup
    print("\nNumber of rows, columns:", supa_df.shape)

    # Remove data point where hint coloumn is missing
    supa_df = supa_df.dropna(subset=['hint'])

    # remove the plot_embedding from each data point in the dataset as we are going to create new embeddings with the new OpenAI emebedding Model "text-embedding-3-small"
    supa_df = supa_df.drop(columns=['hint_embedding'])
    # supa_df.head(5)

    # Step 1: Combine the columns
    supa_df["combined_text"] = supa_df.apply(lambda row: f"{row['problem_name']} {row['code']} {row['hint']}", axis=1)

    # Step 2: Generate the embeddings for the combined text
    supa_df["hint_embedding"] = supa_df["combined_text"].apply(get_embedding) # use the get_embedding method above

    # Drop the combined_text column if not needed anymore
    supa_df.drop(columns=["combined_text"], inplace=True)

    # MONGO DB connection

    # connection_string = f'mongodb+srv://beetcodeai:{MONGO_PASSWORD}@beetcode.mcyrpag.mongodb.net/?retryWrites=true&w=majority&appName=Beetcode'
    connection_string = f'mongodb+srv://beetcodeai:{MONGO_PASSWORD}@cluster0.yuiy7jk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

    # DATABASE_NAME = 'mvp'
    # COLLECTION_NAME = 'hints'

    client = MongoClient(connection_string)

    try:
        print("Connected")
        # client.close()

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)

    # now try inserting a new collection

    # Ingest data into MongoDB
    db = client['hints']
    collection = db['hint_collection']

    # Delete any existing records in the collection
    collection.delete_many({})

    documents = supa_df.to_dict('records')
    collection.insert_many(documents)

    print("Data ingestion into MongoDB completed")

    # DO NOT close client at the end
    # client.close()
    return supabase, collection

# internal method
def vector_search(user_query, collection):
    """
    Perform a vector search in the MongoDB collection based on the user query.

    Args:
    user_query (str): The user's query string.
    collection (MongoCollection): The MongoDB collection to search.

    Returns:
    list: A list of matching documents.
    """

    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."

    # Define the vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "hint_embedding",
                "numCandidates": 150,  # Number of candidate matches to consider
                "limit": 1  # Return top 1 matches
            }
        },
        {
            "$project": {
                "_id": 0,  # Exclude the _id field
                "problem_name": 1,  # Include the plot field
                "code": 1,  # Include the title field
                "hint": 1, # Include the genres field
                "rating": 1, # Include the genres field
                "score": {
                    "$meta": "vectorSearchScore"  # Include the search score
                }
            }
        }
    ]

    # Execute the search
    results = collection.aggregate(pipeline)
    return list(results)

@app.route('/edit_rating', methods=["GET", "POST"]) # NVM ITS A POST REQUEST
def edit_rating():
    hint_generated = request.json.get('hint_generated', '')
    # problem_name = request.json.get('problem_name', '') DO NOT NEED PROBLEM NAME ANYMORE
    # current_code = request.json.get('problem_code', '')
    
    rating_change = request.json.get('like', '')
    rating_change = int(rating_change)

    return {
        'success': True
    }

# if the user hits the "like" endpoint here
# @app.route('/edit_rating', methods=["GET", "POST"]) # NVM ITS A POST REQUEST
def edit_rating_old():
    # get the hint generated from FE
    hint_generated = request.json.get('hint_generated', '')
    # problem_name = request.json.get('problem_name', '') DO NOT NEED PROBLEM NAME ANYMORE
    # current_code = request.json.get('problem_code', '')
    
    rating_change = request.json.get('like', '')
    rating_change = int(rating_change)

    # like must be 1 for true (like)
    # or -1 for false (dislike)

    # example: "Let’s first break down the known parameters. We have two lists (nums1, nums2) and two numbers (m, n) indicating the size of those lists. How can we use this information to iterate over the elements?"
    supabase, collection = update_embeddings()
    
    get_knowledge = vector_search(hint_generated, collection)
    
    # NEED TO SET UP COLLECTION FOR MONGODB!!!

    for result in get_knowledge: # should just be one item
        # search_result += f'''Problem: {result.get('problem_name', 'N/A')} \n\nCode: {result.get('code', 'N/A')} \n\nHint: {result.get('hint', 'N/A')} \n\n'''
        
        problem_name = result.get('problem_name', 'N/A')
        code = result.get('code', 'N/A')
        hint = result.get('hint', 'N/A')
        rating = result.get('rating', 'N/A')

        score = result.get('score', 'N/A')
        print("Closest Search Score: " + str(score))

        if score <= COSINE_THRESHOLD: # then no close match
            # add problem, code, hint to DB (supabase)
            # make the rating equal to 1, -1

            data, count = supabase.table('hints').insert({"problem_name": problem_name,
                                                          "code": code,
                                                          "hint": hint_generated,
                                                          "rating": rating_change}).execute()

            # now re-run the method that generates the embeddings and saves in the MongoDB database
            _,_ = update_embeddings()
                        
        else:
            # there is a close match, so identify the 3 relevant params (problem name, code, hint)
            problem_name = result.get('problem_name', 'N/A')
            code = result.get('code', 'N/A')
            hint = result.get('hint', 'N/A')
            rating = result.get('rating', 'N/A')

            # Increment or decrement the rating value
            new_rating = rating + rating_change

            # Update the table with the new rating
            # Maybe just find the close hint, should be enough?

            data, count = (
                supabase.table('hints')
                .update({'rating': new_rating})
                .eq('problem_name', problem_name)
                .eq('code', code)
                .eq('hint', hint)
                .execute()
            )
    
    return {
        'success': True
    }

if __name__ == '__main__':
   app.run(port=8001, debug=True)
   # app.run()