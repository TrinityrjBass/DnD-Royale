"""
Routes and views for the flask application.
"""
import csv
import json
import os
import threading, time
from datetime import datetime
from flask import render_template, request
from . import app, DnD, creature


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
        list=sendindex()
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# I don't think I like this here
def sendindex():
    """ loads creatures from beastiary file and populates dropdown menu on page"""
    print("SendIndex") #for debugging
    # Read creatures from bestiary  
    #root = 'static/content/'
    #creaturelist =creature.Creature.load_beastiary('DnDRoyale/creatures.csv')
    creaturelist = ''
    with open('DnDRoyale/creatures.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        xp = []
        for row in reader:
            if line_count == 0:
                # skip column names
                line_count+=1
            else:
                #get data from row as row[column]
                # put data in html tags
                # add name to list
                creaturelist += '<option data-xp="'+ row[23] +'" value="'+row[0]+'">'+row[0]+'</option>'
                line_count+=1

    # x='<!--serverside values-->'
    # Add creatures to html dropdown list
    #for name in sorted([creature.Creature.beastiary[beast]['name'] for beast in creature.Creature.beastiary],key=str.lower):
    #    x+='<option value="'+name+'">'+name+'</option>,'
    #x.split(',')
    #response_body=response_body.replace("<!--LABEL-->",x)
    #response_body = response_body.encode('utf-8')

    return creaturelist


#from the encounter simulator app
@app.route('/poster/', methods=['POST'])
def poster():              
    #from cgi import parse_qs
    print("We've hit the Poster!");
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
        #l = request.values
        # need to find the right way to parse the list from request
        # print("l : " + l)
        wwe = DnD.Encounter(*l)
        w=threading.Thread(target=wwe.go_to_war,args=(5,)) #default is 1000, changing to 5 for testing
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

#if __name__ == '__main__':
#    app.run(debug=True)
# I don't think this is needed... maybe
