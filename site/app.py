from flask import Flask, render_template, request, redirect, flash
import os, dbcontroller, hashlib

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "static/uploads/"
app.config['MAX_CONTENT_LENGTH'] = 50 * (1024 ** 2) #50 MB for every file

ALLOWED_FORMATS = {"docx","pptx","xlsx","pdf"}
def fileIsAllowed(filename): return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_FORMATS

@app.route("/")
def index(): return render_template("index.html")

@app.route("/signup", methods=["GET"])
def signup_view(): return render_template("register.html", mode="signup")

@app.route("/signup", methods=["POST"])
def signup():
	#TODOs:
	#  1. check for id don't be exist [DONE]
	#  2. check the lengths of values [!REQUIRE]
	#  3. making folder for every  id [DONE]
	db = dbcontroller.io("users.db")
	db.makeStorage()
	ID = request.form.get("id")
	email = request.form.get("email")
	password = request.form.get("password")
	
	IDs = [i[0] for i in db.readStorage()]
	if not ID in IDs:
		db.writeStorage((
			ID,
			email,
			hashlib.sha256(password.encode()).hexdigest()
		))
		db.closeStorage()
		try: os.mkdir(app.config['UPLOAD_FOLDER']+ID)
		except FileExistsError : pass
		return "200"
	db.closeStorage()
	return "400"
	

@app.route("/login", methods=["GET"])
def login_view(): return render_template("register.html", mode="login")

@app.route("/login", methods=["POST"])
def login():
	db = dbcontroller.io("users.db")
	items = db.readStorage()
	password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
	for i in items:
		if i[0] == request.form.get("id") and hashlib.sha256(i[2].encode()).hexdigest() == password: return "200"
	db.closeStorage()
	return "400"

@app.route("/upload/<to>", methods=["POST"])
def upload(to):
	args = [request.form[i] for i in request.form]
	file = request.files["file"]
	if file and fileIsAllowed(file.filename):
		try: os.mkdir(app.config['UPLOAD_FOLDER']+args[0]+"/"+to)
		except FileExistsError : pass
		filename = str(args[0]+"/"+file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return "200"
	else:
		return "403"

@app.route("/reserve", methods=["POST"])
def reserve(): pass

@app.route("/todos", methods=["POST"])
def getTodoList():
	password = request.form.get("password")
	if password == "00475c6f6d939ecbc6aaa1b650236366c4f5aa79e958b5c151196ba6187c153d":
		db = dbcontroller.todosIO("todos.db")
		db.makeStorage()
		result = db.readStorage()
		db.closeStorage()
		return str(result)
	else:
		return "403"

app.run(debug=True)