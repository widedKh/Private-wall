# __init__.py
from flask import Flask,render_template, request,redirect
app = Flask(__name__)
app.secret_key = "shhhhhh"

DATABASE = "private_wall"
