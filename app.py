
from flask import Flask, request, redirect, render_template, url_for
from flask import session as login_session

from textblob import TextBlob
import pyrebase

config = {
  "apiKey": "AIzaSyAzOryQu2GKKpjrLJd6XiHovIBcaPbHiSI",
  "authDomain": "travel-e4397.firebaseapp.com",
  "databaseURL": "https://travel-e4397-default-rtdb.europe-west1.firebasedatabase.app/",
  "projectId": "travel-e4397",
  "storageBucket": "travel-e4397.appspot.com",
  "messagingSenderId": "135115585574",
  "appId": "1:135115585574:web:c23640a5b1394edc5e0ee7",
  "measurementId": "G-RCSB6KC2N6"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'




@app.route('/')
def home():
	return render_template('index.html', )


@app.route('/about.html')
def About():
	return render_template('about.html')


@app.route('/upload.html' , methods=['GET','POST'])
def upload():
	if request.method == 'GET' :
		return render_template('upload.html')
	else:
		print("creating Place object")
		name_of_place = request.form['nameOfplace']
		description = request.form['subject']
		user = request.form['user']
		link = request.form['Link']
		#add_place is a function that creates a new object of a place based on the data that the user has entered in the webstie, and then it sends it to the database as a Place object.
		if len(user) == 0:
			user = "Anonymous User"
		if len(link) == 0:
			link = "https://wallpapercave.com/wp/wp4813075.jpg"

		add_place(name_of_place , description , user , link)
		return redirect('list.html')


@app.route('/list.html')
def fullList():
	places=query_all()
	return render_template('list.html',places=places)

@app.route('/place.html/<int:p_id>')
def place(p_id):
	place=session.query(Place).filter_by(id=p_id).one()
	if TextBlob(place.description).polarity > 0:
		polarity = "Positive!"
	else : 
		polarity = "Negative"
	return render_template('place.html',place=place , polarity = polarity)

@app.route("/login.html")
def login():
	return ("login.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
	error = ""
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		try:
			login_session["user"] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for("home"))
		except:
			error = "Authentication failed"
			print(error)
	return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
	error = ""
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		try:
			login_session["user"] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for("home"))
		except:
			error = "Authentication failed"
	return render_template("signin.html")

@app.route('/signout')
def signout():
	login_session["user"] = None
	auth.current_user = None
	return redirect(url_for("index.html"))

#// Initialize Firebase
#const app = initializeApp(Config);
#const analytics = getAnalytics(app);



if __name__ == '__main__':
	app.run(debug=True)
