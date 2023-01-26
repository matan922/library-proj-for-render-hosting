from flask import render_template, redirect, Blueprint, request
from project import db
from project.clients.models import Clients



client = Blueprint('client', __name__, template_folder='templates',url_prefix='/client')

'''Function that shows clients based on name given in the url's endpoint
or shows all clients if no name was given.
Default is set to show all clients.'''
@client.route("/", methods=['GET'])
@client.route("/<name>")
def client_list(name=""):
    if name == "":
        clients = Clients.query.all()
        return render_template('all_clients.html', clients=clients)
    if name != "":
        single_client = Clients.query.filter(Clients.clientname==name).first()
        return render_template('clients.html', single_client=single_client)

'''Function made to search a specific client based 
on the name given in the url's endpoint from the function above.'''
@client.route("/client_search", methods=['POST'])
def client_name():
    name = request.form['clientname']
    # If the client's name from the html <input> tag matches a name from the database it redirects you to said database client name in the url's endpoint.
    client = Clients.query.filter(Clients.clientname==name).first()
    # If client does not exist you get redirected to the same page that shows all clients.
    if client is None:
        return redirect('/client')
    return redirect(f"{client.clientname}") 

# Function made to render a page where a user can add a new client to the library.
@client.route("/add_client")
def add_client_page():
    return render_template("add_client.html")

# Function made to add a new client from the page created by previous function.
@client.route("/", methods=['POST','GET'])
def add_client():
    if request.method == 'POST':
        # Making a form that connects to the <form> html tag for user input.
        request_data = request.form
        clientname = request_data["clientname"]
        age = request_data["age"]
        city = request_data["city"]
        new_customer = Clients(clientname,age,city)
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/client')

# Function made to delete a client from the database based on the index (id) of the client.
@client.route("/client_del", methods=['GET','DELETE'])
@client.route("/client_del/<ind>")
def client_del(ind):
    client = Clients.query.get(int(ind))
    # If the client does not exist return to the endpoint that shows all clients.
    if client is None:
        return render_template('all_clients.html', clients=Clients.query.all())
    try:
        db.session.delete(client)
        db.session.commit()
    except:
        return render_template('all_clients.html', clients=Clients.query.all())
    return render_template('all_clients.html', clients=Clients.query.all())
    # After function is done running it will render the page that shows all clients.

