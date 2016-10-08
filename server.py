from flask import Flask, render_template, request, redirect, flash
# import the Connector function
from mysqlconnection import MySQLConnector

# import regex stuff
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "mysecretkey"

# connect and store connection in mysql
mysql = MySQLConnector(app, 'full_friends')


@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends_list = mysql.query_db(query)
    return render_template('index.html', friends_list=friends_list)


@app.route('/friends', methods=['POST'])
def friends():
    if len(request.form['email']) < 1 or len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1:
        flash("Please fill out all boxes!")
    elif not email_regex.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        flash('Added {} in database'.format(request.form['first_name'], request.form['last_name']))
        query = "INSERT INTO friends (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, Now());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }
        mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
    print(id)
    query = "SELECT first_name, last_name FROM friends WHERE id=:id"
    data = {
        'id': id
    }
    friend = mysql.query_db(query, data)[0]
    print(friend)
    # flash('deleted {} {} from your database',format(friend.first_name, friend.last_name))
    # query = "DELETE FROM friends WHERE id=:id"
    # #mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
