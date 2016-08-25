""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def process_user_registration(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        messages = []
        #check to see if the user email already exists.
        login_user_query = '''SELECT * FROM users WHERE email=:email LIMIT 1 '''
        data={
        'email': info['email']
        }
        login_user = self.db.query_db(login_user_query, data)
        if (login_user):
            messages.append("User with that email already exists.")
            return {'status': False, 'messages': messages}
        #If the email is not already registered, validate the other forms.
        if not info['first_name']:
            messages.append('Name cannot be blank')
        if len(info['first_name']) < 2:
            messages.append('Name must be at least 2 characters long')
        if not info['email']:
            messages.append('Email cannot be blank')
        if not EMAIL_REGEX.match(info['email']):
            messages.append('Email format must be valid!')
        if not info['password']:
            messages.append('Password cannot be blank')
        if len(info['password']) < 8:
            messages.append('Password must be at least 8 characters long')
        if info['password'] != info['password_confirm']:
            messages.append('Password and confirmation must match!')
        # If we hit messages, return them, else return True.
        if messages:
            return {"status": False, "messages": messages}
        else:
            messages.append('Successfully Registered! Use the form on the right to log in.')
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            insert_user_query = "INSERT into users (first_name, last_name, email, pw_hash, created_at, updated_at) values(:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"
            data = {'first_name': info['first_name'],
            'last_name': info['last_name'],
            'email': info['email'],
            'pw_hash': pw_hash,
            }
            user = self.db.query_db(insert_user_query, data)
            return {"status": True, "messages": messages}
    def process_user_login(self, info):
        errors=[]
        login_user_query = '''SELECT * FROM users WHERE email=:email LIMIT 1 '''
        data={
        'email': info['email']
        }
        log_in_user = self.db.query_db(login_user_query, data)
        if (log_in_user and self.bcrypt.check_password_hash(log_in_user[0]['pw_hash'], info['log_in_password'])):
            return {'status': True, 'log_in_user':log_in_user}
        else:
            errors.append("Wrong email or password.")
            return {'status': False, "errors": errors}
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)
