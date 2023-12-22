from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')   
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d).+$")

class User:
    def __init__( self , data ):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.messages=[]
      
    @staticmethod
    def validate_user( user ):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(DATABASE).query_db(query,user)
            
        is_valid = True
        # test whether a field matches the pattern
        if len(user['fname']) < 3:
            flash("First Name must be at least 3 characters!","register")
            is_valid = False
        if len(user['lname']) < 3:
            flash("Last Name must be at least 3 characters!","register")
            is_valid = False    
        if user['pwd'] != user['conf_pwd']:
            flash("Invalid password!","register")
            is_valid = False
        elif len(user['pwd']) < 3:
            flash("Password must be at least 8 characters!","register")
            is_valid = False
        elif not PASSWORD_REGEX.match(user['pwd']): 
            flash("Password must have at least one number and one uppercase letter!","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        if result: 
            flash("Email already exist!","register")
            is_valid = False
        return is_valid
    
    
    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s order by first_name;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        users = []
        for user in results:
            users.append( cls(user) )
  
        return users
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
           return cls(result[0])
        return result
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at ) VALUES ( %(fname)s, %(lname)s, %(email)s ,%(pwd)s, NOW() , NOW() );"
        return connectToMySQL(DATABASE).query_db( query, data )        
