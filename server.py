from flask import Flask, render_template, request, redirect, flash
# import the Connector function
from mysqlconnection import MySQLConnector

#import regex stuff
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "mysecretkey"

#connect and store connection in mysql
mysql = MySQLConnector(app, 'full_friends')

@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends_list = mysql.query_db(query)
    return render_template('index.html', friends_list=friends_list)

# @app.route('/validate', methods=['POST'])
# def validate_email():
#     if len(request.form['email']) < 1:
#         flash("Email cannot be blank!")
#         return redirect('/')
#     elif not email_regex.match(request.form['email']):
#         flash("Invalid Email Address!")
#         return redirect('/')
#     else:
#         flash("The email address you entered ({}) is a VALID email address! Thank you!".format(request.form['email']))
#         query = "INSERT INTO emails (emails, created_at, updated_at) VALUES (:email, Now(), Now())"
#         data = {
#             'email': request.form['email']
#         }
#         mysql.query_db(query, data)
#         return redirect('/success')
# @app.route('/success')
# def show_emails():
#     query = "SELECT emails, date_format(created_at, '%m:%d:%y %l:%i %p') as created_at FROM emails"
#     emails = mysql.query_db(query)
#     return render_template('emails.html', emails=emails)

app.run(debug=True)
