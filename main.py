"""
Main Controller for Web Application assignment (ITEC649)

@author: Shashank Salunkhe

"""

from bottle import Bottle, static_file, template , request, redirect
import interface,users

app = Bottle()

@app.route("/")
@app.route(("/index.html"))
def index(db):
    """
    index method for routing on index.html and homepage '/'
    :param db: Accepts db conncetion
    :return: index page template
    """
    positions = interface.position_list(db,10) # Calling position_list method which returns list of tuples - positions
    # method returns most recent 10 positions ordered by date which is then passed to the view for displaying

    active_user = users.session_user(db) # Fetching active user name
    message = dict() #Creating dictionary entry for message passing.
    message["positions"] = positions
    message["user"] = active_user
    message["title"] = "Jobs Home"
    return template("index" , message = message)

@app.route("/about.html")
def about(db):
    """
    :return: Returns a static template page about.html when the request is made to the server for route '/about.html'
    """
    active_user = users.session_user(db)
    message = dict() # Creating dictionary entry for message passing which can be accessed in html.
    message["user"] = active_user
    message["title"] = "About this site"
    return template("about", message=message)

@app.route("/static/<filepath:path>")
def server_static(filepath):
    """
    Used to render the static files in the project.
    We import static_file handler from Bottle and pass it the path and location of root dir
    """
    return static_file(filename=filepath, root="static")

@app.post("/login")
def login(db):
    # Method to handle login action of form.
    # Field values are validated for null values by html required property.
    #First checking if the login is succes for the provided username and password combination. If success, then create
    # a session  and redirect it to the index page.
    # If username - password combination is invalid, then redirect the request to fail.html

    username = request.forms.get('nick')
    password = request.forms.get('password')
    login_check = users.check_login(db,username,password)
    if login_check:
        users.generate_session(db,username) #calling generate_session method from users module
        return redirect("/")
    else:
        return template("fail" , title = "Login Failed")


@app.post("/logout")
def logout(db):
    # Method to logout.
    # First checking if the active user is logged in or not. If the user is logged in and has an active session, then
    # deleting the session from sessions table and redirecting to the index page.
    active_user = users.session_user(db)
    if active_user is not None:
        users.delete_session(db,active_user)
    return redirect("/")

@app.post("/post")
def post_job(db):
    # Method to persist job. Method handles form request from "/post" and then extracts individual components
    # Calls position_add method from interface module to persist it to the db

    title= request.forms.get("title")
    company = request.forms.get("company")
    location = request.forms.get("location")
    description = request.forms.get("description")
    active_user = users.session_user(db)
    interface.position_add(db,active_user,title,location,company,description)
    redirect("/") # Redirecting to the index page

@app.route("/positions/<id>")
def display_job(db,id):
    """
    :param id: Takes id as parameter from the 'Read more' hyperlink. This id is the unique id of job position.
    :return: Returns template page position.html when request is made to the server for route '/position/DD' where DD is
    the particular id
    """
    position = interface.position_get(db,id) # Calling position_get method which returns all the details of the particular
    #job position

    active_user = users.session_user(db)
    message = dict() # Creating dictionary entry
    message["user"] = active_user
    message["title"] = "Job Position"
    return template("position", message=message , position = position)


if __name__=="__main__":
    #Main function is called to run the application.
    from bottle.ext import sqlite
    from database import DATABASE_NAME
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True,port=8010)