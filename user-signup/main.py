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

    if user_name =='':
        username_error = "Must enter Username with more than 3 characters and less than 20, no spaces."
        return template_username.render(username_error = username_error)
    if len(user_name) < 3 or len(user_name) > 20:
        username_error = "Must enter Username with more than 3 characters and less than 20, no spaces."
        return template_username.render(username_error=username_error)
    for character in user_name:
        if character == ' ':
            username_error = "No spaces in username"
            return template_username.render(username_error=username_error)

    if password == '':
        password_error = "Must enter a password with more than 3 characters and less than 20, no spaces."
        return template_username.render(password_error=password_error)
    if len(password) < 3 or len(password) > 20:
        password_error = "Must enter password with more than 3 characters and less than 20, no spaces."
        return template_username.render(password_error=password_error)

    if same_password != password:
        different_password_error = "Verify if password is the same and re-enter"
        return template_username.render(different_password_error=different_password_error)

    if email != '' and ('@'not in list(email) or '.' not in list(email)):
        email_error = "Please enter valid email"
        return template_username.render(email_error=email_error)
    
    return template_greeting.render(username=user_name)


@app.route('/validate-time')
def display_time_form():
    template = jinja_env.get_template('time_form.html')
    return template.render()


def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
        

@app.route('/validate-time', methods=['POST'])
def validate_time():

    user_name = request.form['username']
    #minutes = request.form['minutes']

    username_error = ''
    #minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = 'Hour value out of range (0-23)'
            hours = ''

    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'Minutes value out of range (0-59)'
            minutes = ''

    if not minutes_error and not hours_error:
        time = str(hours) + ':' + str(minutes)
        return redirect('/valid-time?time={0}'.format(time))
    else:
        template = jinja_env.get_template('time_form.html')
        return template.render(hours_error=hours_error,
            minutes_error=minutes_error,
            hours=hours,
            minutes=minutes)


@app.route('/valid-time')
def valid_time():
    time = request.args.get('time')
    return '<h1>You submitted {0}. Thanks for submitting a valid time!</h1>'.format(time)

app.run()