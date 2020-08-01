


#def sendindex():
#    """ loads creatures from beastiary file and populates dropdown menu on page"""
#    print("SendIndex") #for debugging
#    # Read creatures from bestiary  
#    creature.Creature.beastiary=creature.Creature.load_beastiary(static/content/+'beastiary.csv')
#    ctype = 'text/html'
#    h=open(apppath+"index.html")
#    response_body = h.read()
#    x='<!--serverside values-->'
#    # Add creatures to html dropdown list
#    for name in sorted([creature.Creature.beastiary[beast]['name'] for beast in creature.Creature.beastiary],key=str.lower):
#        x+='<option value="'+name+'">'+name+'</option>,'
#    x.split(',')
#    response_body=response_body.replace("<!--LABEL-->",x)
#    response_body = response_body.encode('utf-8')

#    return response_body
