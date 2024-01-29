# Import the Flask class from the flask module
import mysql.connector
from flask import Flask, render_template,request

# Create an instance of the Flask class
app = Flask(__name__)



mysql_config = {
    'host': 'localhost',  # Change this to your MySQL server host
    'user': 'root',  # Change this to your MySQL username
    'password': 'root',  # Change this to your MySQL password
    'database': 'gas'  # Change this to your MySQL database
}
db_connection = mysql.connector.connect(**mysql_config)


# Define a route for the root URL ('/')
@app.route('/')
def index():
    # Render the HTML template 'index.html'
    return render_template('index.html')



@app.route("/login",methods=["GET","POST"])
def login():


    if(request.method == "POST"):
        print(request.form)
        name = request.form.get("email")
        password = request.form.get("password")
        print(name)
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT password FROM users where name='{name}'")
        data = cursor.fetchall()
        print("insd=ide")
        if data[0][0] == password :
            return render_template("index.html",name=name)
        else:
            return "login failed"

    else:
        return render_template("login.html")



@app.route("/book/<id>",methods=["POST","GET"])
def book(id):

    if request.method == "POST":

        userid = request.form.get("userid",1)
        techid=request.form.get("techid")
        description = request.form.get("description").strip()
        print(userid,techid,description)
        cursor = db_connection.cursor()
        print(f"INSERT INTO booking (userid, technid, description) values ({userid},{techid},'{description}')")
        cursor.execute(f"INSERT INTO booking (userid, technid, description) values ({userid},{techid},'{description}');")
        db_connection.commit()

        data = cursor.fetchall()
        return data

    else:
        return render_template("book.html",techid=id)


@app.route("/showtechnicians")
def shoetech():
    service = request.args.get("service")
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT * FROM services where servicetype='{service}'")
    data = cursor.fetchall()

    return render_template("showtech.html",data=data)




# Run the app if the script is executed
if __name__ == '__main__':
    # Set the host to '0.0.0.0' to make the app accessible from external devices
    app.run(host='0.0.0.0', port=5000, debug=True)
