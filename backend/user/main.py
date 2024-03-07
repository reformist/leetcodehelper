import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
app = Flask(__name__)