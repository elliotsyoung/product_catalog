""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """
    def get_products(self):
        query = "SELECT * from products"
        return self.db.query_db(query)

    def get_product(self, id):
        query= '''SELECT * from products where id=:id'''
        data = {
        'id': id
        }
        return self.db.query_db(query, data)

    def add_product(self, info):
        sql = "INSERT into products (name, description, price, created_at, updated_at) values(:name, :description, :price, NOW(), NOW())"
        data = {
        'name': info['name'], 
        'description': info['description'], 
        'price': info['price']}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)
    def edit_product(self, info):
        query = '''UPDATE products SET name=:name, description=:description, price=:price, updated_at=NOW() WHERE id=:id'''
        data= {
        'name': info['name'],
        'description': info['description'],
        'price': info['price'],
        'id': info['id']
        }
        return self.db.query_db(query, data)
    def delete_product(self, id):
        query = '''DELETE FROM products WHERE id=:id'''
        data= {
        'id': id
        }
        return self.db.query_db(query, data)
