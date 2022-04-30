"""
Routes and views for the flask application.
"""
import csv
import json
import os
import threading, time
from datetime import datetime
from tkinter.dnd import dnd_start
from flask import render_template, request
from . import app, DnD

#app.debug = True
#from DnDRoyale import creature
print("loading views file")

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    sendindex()
    return render_template(
        'index.html',
        title='D&D Battle Simulator',
        list=sendindex(),
        year=datetime.now().year
    )

@app.route('/contact') #legal
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Legal, ' + os.getcwd(),
        year=datetime.now().year,
        message='Legal Notice'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='...About.'
    )

# I don't think I like this here
def sendindex():
    """ loads creatures from beastiary file and populates dropdown menu on page"""
    print("SendIndex") #for debugging
    # Read creatures from bestiary  
    
    creaturelist = ''
    beastiary = DnD.creature.Creature.beastiary

    for row in beastiary:
        beast = beastiary[row]
        creaturelist += '<option data-xp="'+ beast['xp'] +'" value="'+beast['name']+'">'+beast['name']+'</option>'
    return creaturelist

#from the encounter simulator app
@app.route('/poster/', methods=['POST'])
def poster():              
    request_body = ""
    list = "" 
    
    try:
        request_body_size = request.environ['CONTENT_LENGTH']
        #list = json.loads(request.json)
        #print("request body : " + request.form.read(request_body_size))
        #request_body = request.environ['wsgi.input'].read(request_body_size)
    except (TypeError, ValueError):
        request_body = "0"
        print("No request found")

    try:
        l = json.loads(request.data)
        wwe = DnD.Encounter(*l)
        w=threading.Thread(target=wwe.go_to_war,args=(1000,)) #default is 1000, changing to 5 for testing
        w.start()
        time.sleep(10)
        wwe.KILL = True
        response_body = wwe.battle(1, 1).json()
        #add_to_tales(wwe)
    except Exception as e:
        print(e)
        response_body = json.dumps({'battles':"Error: "+str(e)})
    ctype = 'text/plain'
    response_body = response_body.replace("\n","<br/>")
    response_body = response_body.encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    print("resopnse body : " + str(response_body))

    return response_body

