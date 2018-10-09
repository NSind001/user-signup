from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('username.html')
    return template.render()

@app.route("/username", methods=['POST'])
def username():
    template_greeting = jinja_env.get_template('hello_greeting.html')
    template_username = jinja_env.get_template('username.html')

    user_name = request.form['username']
    password = request.form['password']
    same_password = request.form['same_password']
    email = request.form['email']

    username_error=''
    password_error=''
    different_password_error=''
    email_error=''
    error = 0

    if user_name =='':
        username_error = "Must enter Username with more than 3 characters and less than 20, no spaces."
        error += 1
        #return template_username.render(username_error = username_error)
    if len(user_name) < 3 or len(user_name) > 20:
        username_error = "Must enter Username with more than 3 characters and less than 20, no spaces."
        error += 1
        #return template_username.render(username_error=username_error)
    for character in user_name:
        if character == ' ':
            username_error = "No spaces in username"
            error += 1
            #return template_username.render(username_error=username_error)

    if password == '':
        password_error = "Must enter a password with more than 3 characters and less than 20, no spaces."
        error += 1
        #return template_username.render(password_error=password_error)
    if len(password) < 3 or len(password) > 20:
        password_error = "Must enter password with more than 3 characters and less than 20, no spaces."
        error += 1
        #return template_username.render(password_error=password_error)

    if same_password != password:
        different_password_error = "Verify if password is the same and re-enter"
        error += 1
        #return template_username.render(different_password_error=different_password_error)

    if email != '' and ('@'not in list(email) or '.' not in list(email)):
        email_error = "Please enter valid email"
        error += 1
        #return template_username.render(email_error=email_error)
    
    if error > 0:
        return template_username.render(username_error=username_error, password_error=password_error, different_password_error=different_password_error, email_error=email_error, username=user_name, email=email)
    else:
        return template_greeting.render(username=user_name)

app.run()