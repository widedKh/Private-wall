from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import DATABASE
from flask_app.models import user

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')   
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d).+$")

class Message:
    def __init__( self , data ):
        self.id= data['id']
        self.content= data['content']
        self.sender_id= data['sender_id']
        self.receiver_id= data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
      
    @staticmethod
    def validate_message( message ):
        print("len message",len(message['content']))
        is_valid = True
        # test whether a field matches the pattern
        if len(message['content'].strip()) < 3:
            flash("Message should have at least 3 characters!","messages")
            is_valid = False
        
        return is_valid
    
        
    @classmethod
    def get_all_messages_with_time(cls,data):
        # Get all messages, and their one associated User that created it
        query = "SELECT users.first_name as sender, users2.first_name as receiver, timediff(now(),messages.created_at) as time_spent, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
                
        return results
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        emails = []
        for email in results:
            emails.append( cls(email) )
  
        return emails
    
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
    def delete_msg(cls,data):
        query = "delete from messages where id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
          
        return results
    
    @classmethod
    def get_numb_of_msg_received(cls,data):
        query = "select count(*) as nb_msg_rc from messages where receiver_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
          
        return result[0]
    
    @classmethod
    def get_numb_of_msg_sent(cls,data):
        query = "select count(*) as nb_msg_se from messages where sender_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
          
        return result[0]
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO messages ( content, sender_id,receiver_id) VALUES ( %(content)s, %(sender_id)s, %(receiver_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )        
