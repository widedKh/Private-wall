from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.message import Message

    

@app.route('/message/create', methods=['POST'])
def create_message():
    
    data = {
        "content": request.form['content'],
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id']
        
    }
    # validate the form here ...
    if not Message.validate_message(request.form):
        # redirect to the wall 
        return redirect('/wall')
    
    # Call the save @classmethod on Message
    Message.save(data)
    
    return redirect("/wall")

@app.route('/message/delete/<int:msg_id>')
def delete_message(msg_id):
    data = {'id':msg_id}
    Message.delete_msg(data)
    return redirect("/wall")


