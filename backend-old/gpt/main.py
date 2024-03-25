from __future__ import print_function

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import openai
import json
import traceback
import re

import os.path
import sys

import base64

# import statements
from leetscrape import GetQuestionsList, GetQuestion, GenerateCodeStub, ExtractSolutions
from bs4 import BeautifulSoup


load_dotenv(find_dotenv())
app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5000", "http://localhost:3000"]}}) # same port number
CORS(app, resources={r"/*": {"origins": "*"}})

'''
Route to submit problem name, starting code

Generate problem description

Return the hints for the user
'''
@app.route('/hints', methods=["GET"]) # GET request, with input params
def get_hints(): # when user submits a request to add event to calendar
    # print(request.method)

    # Retrieve 'problem_name' from query parameters
    problem_name = request.args.get('problem_name', '')

    problem_description = get_problem_description(problem_name)

    print(problem_description)

    try:
        return {
            'success': True,
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
    question = GetQuestion(titleSlug=name).scrape() # e.g. two-sum
    description_html = question.Body

    # Use BeautifulSoup to parse the HTML content and get plain text
    soup = BeautifulSoup(description_html, 'lxml')
    description_text = soup.get_text(separator='\n', strip=True)

    return description_text

