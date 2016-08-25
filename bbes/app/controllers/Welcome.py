"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('WelcomeModel')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        #Set the input fields to blank if the user hasn't already entered values
        if session.get('saved_inputs') is None:
            session['saved_inputs']= {
            'first_name': "",
            'last_name': "",
            'email': "",
            'log_in_email': "",
            }
        print session['saved_inputs'] 
        return self.load_view('index.html', saved_inputs=session['saved_inputs'])
    def register(self):
        #save the inputs so that the user doesn't have to retype them if one is invalid
        session['saved_inputs']={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'password_confirm': request.form['password_confirm']
        }
        #pass the user inputs to the model which checks for validation
        info = session['saved_inputs']
        create_status = self.models['WelcomeModel'].process_user_registration(info)
        #flash the messages that the model passes. These can be errors or a success message
        for message in create_status['messages']:
            flash(message, 'regis_messages')
        #if the registration was successful, reset the registration fields and autofill the email login form
        if create_status['status']:
            session['saved_inputs']= {
            'first_name': "",
            'last_name': "",
            'email': "",
            'log_in_email': request.form['email'],
            } 
        print session['saved_inputs']
        return redirect('/')
    def log_in(self):
        #Save the log in email  in case they mistype the password
        session['saved_inputs']['log_in_email']=request.form['log_in_email']
        #pass the info to the model for validation
        info={
        'email': request.form['log_in_email'],
        'log_in_password': request.form['log_in_password']
        }
        log_in_status = self.models['WelcomeModel'].process_user_login(info)
        #If the email and password are validated then redirect to the success page
        if log_in_status['status']:
            #Save a session variable for the user id for later validation
            session['user_id']=log_in_status['log_in_user'][0]['id']
            print session['user_id']
            return redirect('/welcome/success')
        else:
            for message in log_in_status['errors']:
                flash(message, 'log_in_errors')
            # redirect to the method that renders the form
                return redirect('/')
    def success(self):
        if session.get('user_id'):
            return self.load_view('success.html')
        else:
            flash('You cannot access that page unless you are logged in', 'log_in_errors')
            return redirect('/')
    def log_out(self):
        session.clear();
        flash('You were logged out!', 'log_in_errors')
        return redirect('/')

