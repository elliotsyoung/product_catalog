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
        return self.load_view('index.html',products=self.models['WelcomeModel'].get_products())
    def show(self, id):
        return self.load_view('show.html', product=self.models['WelcomeModel'].get_product(id)[0])
    def edit(self, id):
        return self.load_view('edit.html', product=self.models['WelcomeModel'].get_product(id)[0])
    def process_edit(self, id):
        info={
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'id': id
        }
        self.models['WelcomeModel'].edit_product(info)
        return redirect('/')
    def delete(self, id):
        self.models['WelcomeModel'].delete_product(id)
        return redirect('/')
    def add(self):
        return self.load_view('add.html')
    def process_add(self):
        info ={
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        }
        self.models['WelcomeModel'].add_product(info)
        return redirect('/')
