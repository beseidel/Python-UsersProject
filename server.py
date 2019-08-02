from flask import Flask, render_template, request, redirect, session, flash

from MySQLconnection import connectToMySQL 
# import the function that will return an instance of a connection



app = Flask(__name__)
app.secret_key = "keep it secret"
#flash require a secret key as well as session


# show a page with a form to create a new user
@app.route('/', methods=["GET"])
def index():
    return render_template("new_user_form.html", )

# process user requires an action and redirect
@app.route('/create', methods=["POST"])
def process_user():
    # add user to database
    # print("Post data")
    # print(request.form)
    # fname = request.form['fname']
    # lname = request.form['lname']
    # em= request.form['email']
    # return render_template("show_one_user.html", fname='first_name', lname='last_name', em='email')
    # connect to to the MySQL schema name
    
    # #this is telling the computer to find the table name users 
    query = "INSERT INTO users_table (first_name,last_name, email, created_at,updated_at) VALUES ( %(fn)s, %(ln)s, %(em)s, NOW(), NOW() );"
    #users_table has the above variables..first_name, last_name, etc and we are setting these variables in the database to be %(fn)s.
    # #fname is the variable name from the form and fn is from whatever we create the variable to be and first_name is what I have in database. 
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
# to the form dictionary where the name field is set to variable fname
    db=connectToMySQL("users")
    user_id = db.query_db(query, data)
    # return render_template('/show_one_user.html')
    #this prints it to show the show_one_user
    return redirect('/show_one_user/' + str(user_id))
  #change this route in the futureto users/create/show_one_user

@app.route('/show_one_user/<id>', methods=['GET'])
def show_one_user(id):
    #to get info about a specific user, you need to pass in an id through the browser

    # return render_template (show_one_user.html)
    #for temporary solution use this render_template

    MySQL = connectToMySQL("users")
    #connect to to the MySQL schema name
    db = connectToMySQL
    #connection to the database can be done any time before the call to the database below. 
    query = "(SELECT * FROM users_table WHERE id_user= %(mickey_id)s);"
    # id_user is the variable name found in the database that intiates a user_id
    print(id)
    #printing the blue id in shown above is id passed in through the browser and not the database.
    
    data = {
        'mickey_id':id
    }  #data is required when we need to define specific data.
    # In this case, id_user in table users_table, there is data for the query to get and this is this data called id which is in blue and it is passed through the both the URL as well as the function above. 
   
    data_id_call = MySQL.query_db(query, data)
    # this is the call to run the function to get the ID in the database where the database will then pass results to the browser page. This database_id is database_id and it will be set to the browswer in orange which will be written in jinja
    return render_template ("show_one_user.html", all_users=data_id_call)        
  #all_users in orange is going to be jinja in the show one user form

#the routing in show_all_users with method GET is to show_all_users
@app.route('/show_all_users', methods=['GET'])
def show_all_users():
    # #make a connection to the database
    # since all users will be shown, then nothing needs to be passed in through the browser or show_all_users function
    MySQL = connectToMySQL("users")
    # get info from db and pass results to the page
    # # # #write a query
    query = "(SELECT * FROM users_table);"
    print(id)
    #do not need to define data because we are requesting all data
    #run query
    #connection to the datapage
    results = MySQL.query_db(query)
    #results is a variable used to define the call in the return statement
    # # # #pass results to the template for rendering
    return render_template ("/show_all_users.html", all_users=results)
    #the orange is what you see in the HTML

# # show the form to edit specific users
@app.route('/edit_user/<id>', methods=["GET"])
def show_edit_form(id):
    MySQL = connectToMySQL("users")

    query = "(SELECT * FROM users_table WHERE id_user= %(mickey_id)s);"
    print(id)
    # this is the id above which is passed through the browser.
    data = {
        'mickey_id': id
        #mickey_id is an id that we set so that the id_user in database matches the id in blue that goes to the browser.
    } 
    # # # # #run query
    users = MySQL.query_db(query, data)
    return render_template("edit_form.html", all_users=users)

@app.route('/edit_user/<id>', methods=['POST'])
def process_edit(id):
    #browser and forms like an id that is a string
    # #     print(<id>)
        # print(id)
    # #connect to db to show users info in the form
    MySQL = connectToMySQL("users")
    # # # # # #write query for getting specific users
 
    query = "UPDATE users_table SET first_name = %(fn)s,last_name=%(ln)s, email=%(em)s, created_at = NOW(), updated_at = NOW() WHERE id_user = %(mickey_id)s;"

    data = {
    "fn": request.form["fname"],
    "ln": request.form["lname"],
    "em": request.form["email"],
    "mickey_id": id
    #if this is a message like in the wall or a hidden input, then request.form['id'] would be required to access it.  
    }
    # #possibly a value from the url,

    MySQL.query_db(query, data)
   
   # where to go after this is complete
    return redirect('/edit_user/' + str(id))
    #need to convert to a string since the browser understands strings.
   
    #orange is what you do in the HTML

@app.route('/delete/<id>', methods=['GET'])
def process_delete(id):
    #     print('user to ??')
    MySQL = connectToMySQL("users")

    # #write an UPDATE query
    query = "DELETE from users_table WHERE ID_user = %(mickey_id)s;"
    print(id)
    
    data = {
        'mickey_id': id
        # if id is from a form unlike this case where there is no form for id, then you will need to do a request.form like above for hidden inputs or like in the messages inthe wall. 
    }
    MySQL.query_db(query, data)
    flash("removed")
    return redirect ('/show_all_users')

if __name__ == "__main__":
    app.run(debug=True)

