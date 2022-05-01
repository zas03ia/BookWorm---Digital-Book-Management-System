from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_mail import Mail, Message
import sqlite3
import time
import random
import re
import os

# Configure app
template_dir = os.path.abspath('C:/Users/Windows/Documents/CSE470/View/templates')
static_dir = os.path.abspath('C:/Users/Windows/Documents/CSE470/View/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


app.config["MAIL_DEFAULT_SENDER"] = "wormbook081@gmail.com"
app.config["MAIL_PASSWORD"] = "bookworm#1"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "wormbook081@gmail.com"
app.config["DEBUG"] = True

mail = Mail(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.secret_key ="bookworm"

# Connect to database
#do = string, table = string, col=  string, val = tuple, con = list#
def data(do = None, table = None, col = None, val = None, con = None):
    db = sqlite3.connect("C:\\Users\\Windows\\Documents\\CSE470\\Model\\database.db")
    cur = db.cursor()
    if do=="select":
        row = None
        if table!= None:
            if len(con) != 0:
                if table == "dictionary":
                    row = cur.execute(f"SELECT {col} FROM {table} WHERE {con[0]} LIKE ?",(con[1]+"%",)).fetchall()
                if len(con) == 2:
                    row = cur.execute(f"SELECT {col} FROM {table} WHERE {con[0]} = ?",(con[1],)).fetchall()
                else:
                    row = cur.execute(f"SELECT {col} FROM {table} WHERE {con[0]} = ? AND {con[2]} = ?",(con[1],con[3])).fetchall()
            else:
                row = cur.execute(f"SELECT {col} FROM {table}").fetchall()
        db.commit()
        db.close()
        return row
    if do== "insert":
        key_id = True
        if table!= None and val!=None:
            l = "?,"*(len(val)-1)+"?"
            if col == None:
                cur.execute(f"INSERT INTO {table} VALUES ({l})", val)
            else:
                key_id = cur.execute(f"INSERT INTO {table} ({col}) VALUES ({l})", val)
        db.commit()
        db.close()
        return key_id
    if do == "update":
        if table!= None and col!= None and con!= None and val!= None:
            if len(con)==2:
                cur.execute(f"Update {table} SET {col} = ? WHERE {con[0]} = ?", (val[0], con[1]))
            if len(con)==4:
                cur.execute(f"Update {table} SET {col} = ? WHERE {con[0]} = ? AND {con[2]} = ?", (val[0], con[1], con[3]))
        db.commit()
        db.close()
        return True

    if do == "delete":
        if table!=None and con!= None:
            if len(con)==4:
                cur.execute(f"DELETE FROM {table} WHERE {con[0]} = ? AND {con[2]} = ?", (con[1], con[3]))
            if len(con)==2:
                cur.execute(f"DELETE FROM {table} WHERE {con[0]} = ?", (con[1],))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return


def load():
    d = {}
    dict = data("select", "dictionary", "*", None, [])
    for i in dict:
        d[i[0].lower()]= i[1]
    return d

Dictionary = load()



# Define object-classes
class Person():
    def __init__(self):
        self.username = session["username"]
        self.email = session["email"]
        self.password = session.get("password")
        if session.get("user"):
            self.id = data("select", "person", "id", None, ["username", str(session.get("user"))])[0][0]
            session["id"] = self.id
            self.email = session["email"] = data("select", "person", "email", None, ["username", str(session.get("user"))])[0][0]
        else:
            self.id = None
            session["id"] = None
    def valid(self):
        us = True
        em = True
        pw = True
        if len(data("select", "person", "*", None, ["username",str(self.username)])) == 0:
            us = False
        if len(data("select", "person", "*", None, ["email", str(self.email)])) == 0:
            em = False
        if len(data("select", "person", "*", None, ["password", str(self.password)])) == 0:
            pw = False

        return {"username": us, "email": em, "password": pw}

    def verify(self):
        pw = session.get("password")
        check = 0
        if len(pw) < 8:
            return False
        for i in "#!$":
            if i in pw:
                check += 1
                break
        for i in "1234567890":
            if i in pw:
                check +=1
                break
        for k in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if k in pw:
                check += 1
                break
        if check == 3:
            return True
        return False

    def login(self):
        if len(data("select", "person", "*", None, ["username", str(self.username), "password", str(self.password)])) != 0:
            return True
        return False

    def create_account(self):
        v = self.valid()
        if v["username"] == True or len(self.username) == 0:
            message = "Invalid Username"
            return [False, message]
        if v["email"] == True:
            message = "Account already exists with this email address"
            return [False, message]
        if v["password"] == True or self.verify == False:
            message = "Invalid Password"
            return [False, message]
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if len(self.email) == 0 or not (re.fullmatch(regex, self.email)):
            message = "Invalid Email Address!"
            return [False, message]
        data("insert", "person", "username, email, password", (self.username, self.email, self.password), [])
        key_id = data("select", "person", "id", None, ["username", self.username])[0][0]
        data("insert", "custom", None, (key_id, "white", "20px", "black"), [])
        return [True]

    def reset(self, start, res_code, return_code):
        stop = time.time()
        if stop - start > 320 or str(res_code) != return_code:
            return [False,"Invalid code!"]
        if self.verify() == False or self.valid()["password"]==True:
            return [False,"Invalid password!"]
        data("update", "person", "password", (session.get("password"),), ["email", str(self.email)])
        return [True]



###########################################################################################
class Book():
    def __init__(self):
        self.id = session["book_id"]

    @classmethod
    def info(cls, user = None):
        if session.get("user"):
            load_per = data("select", "relation", "book_id", None, ["user_id", session["id"]])
            load_total = data("select", "books", "id", None, [])
            for i in load_per:
                if i in load_total:
                    load_total.remove(i)
            books = []
            for l in load_total:
                books += data("select", "books", "id, title, author, year", None, ["id", l[0]])
            return books

        books = data("select", "books", "id, title, author, year", None, [])
        return books

    @classmethod
    def set_progress(cls, p):
        data("update", "relation", "progress", (p,), ["user_id", session["id"], "book_id", session["book_id"]])
        return

    def open(self):
        book = data("select", "books", "title, content", None, ["id", self.id])
        lines = book[0][1].split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip().split(" ")
        return [book[0][0], lines]

    def progress(self):
        prog = data("select", "relation", "progress", None, ["user_id", session.get("id"), "book_id", self.id])
        return prog[0][0]

    @classmethod
    def mean(cls, lines):
        d={}
        for line in lines:
            for word in line:
                word2 = word.lower()
                while (True):
                    if len(word2)==0:
                        break
                    if word2[len(word2)-1] in "abcdefghijklmnopqrstuvwxyz":
                        break
                    word2 = word2[0:-1]
                if word2 in Dictionary.keys():
                    meaning = Dictionary[word2]
                    d[word] = meaning.split("##")
        return d

class Shelf():

    @classmethod
    def show(cls):
        shelf=[]
        load = data("select", "relation", "book_id, progress", None, ["user_id", session.get("id")])
        if len(load)!=0:
            for i in load:
                book = data("select", "books", "title, author, year", None, ["id", i[0]])[0]
                shelf+=[{"id": i[0], "title": book[0], "author": book[1], "year": book[2] , "progress": i[1]}]
        return (shelf, len(shelf))


    @classmethod
    def add_book(cls, b_id):
        ## Add book to personal db
        if session.get("user"):
            if len(data('select', 'relation', '*', None, ['user_id', session["id"], 'book_id', b_id])) == 0:
                data("insert", "relation", None, (session.get("id"), b_id, 0), [])
        return

    @classmethod
    def rm_book(cls, b_id):
        ## remove book from personal db
        if session.get("user"):
            data("delete", "relation", None, None, ['user_id', session.get("id"), 'book_id', b_id])
        return



class Custom():

    @classmethod
    def show(cls):
        custom = data("select", "custom", "background, textsize, textcolor", None, ["id", session.get("id")])
        return custom

    @classmethod
    def set_font_size(cls, size):
        data("update", "custom", "textsize", (size,), ["id", session.get("id")])
        return

    @classmethod
    def set_page_color(cls, p_color):
        data("update", "custom", "background", (p_color,), ["id", session.get("id")])
        return

    @classmethod
    def set_text_color(cls, t_color):
        data("update", "custom", "textcolor", (t_color,), ["id", session.get("id")])
        return




#########################################################



## FLASK routes defined
@app.route("/")
def index():
    if session.get("user"):
        user = Person()
        books = Book.info(user)
        state = "True"
        return render_template("home.html", books=books, state = state, username = user.username, email = user.email )
    else:
        books = Book.info()
        state = "False"
        return render_template("home.html",  books=books, state = state)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect("/")
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        session["email"] = None
        user = Person()
        if user.login():
            session["user"] = request.form.get("username")
            return redirect("/")
        return render_template("login.html", state = "False", message = "Invalid username or password!")
    return render_template("login.html", state = "True")

@app.route("/create", methods=["GET", "POST"])
def create():
    if session.get("user"):
        session["user"] = None
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["email"] = request.form.get("email")
        session["password"] = request.form.get("password")
        user = Person()
        account = user.create_account()
        if account[0]==True:
            session["user"] = request.form.get("username")
            return redirect("/")
        return render_template("create_account.html", state = "False", message = account[1])
    return render_template("create_account.html", state = "True")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if session.get("user"):
        session["user"] = None
    if request.method == "POST":
        if not request.form.get("resend"):
            session["email"] = request.form.get("email")
        session["username"] = None
        session["password"] = None
        user= Person()
        if session["email"] or request.form.get("resend"):
            if user.valid()["email"] or request.form.get("resend"):
                session["res_code"] = random.randrange(100000,999999)
                memo = Message("Verification Code", sender = "wormbook081@gmail.com", recipients=[user.email])
                memo.body = f"Your BOOKWORM Verification Code: {session.get('res_code')}\nReset your password within 5 minutes otherwise the code will expire."
                mail.send(memo)
                session["start"] = time.time()
                return render_template("reset.html", state = "2", message = "Verification code sent! It will expire in 5 minutes")
            return render_template("reset.html", state = "e_False", message = "No user account with this email address")
        else:
            if session["email"] == '':
                return render_template("reset.html", state = "e_False", message = "Please provide an email address")
            else:
                session["return_code"] = request.form.get("verification code")
                session["password"] = request.form.get("password")
                reset_return= user.reset(session.get("start"), session.get("res_code"), session.get("return_code"))
                if reset_return[0]:
                    session["start"]=None
                    session["res_code"]=None
                    session["return_code"] = None
                    return render_template("login.html", state = "False", message = "Reset Password Successful! You may log in!")
                return render_template("reset.html", state = "2_False", message = reset_return[1])
    return render_template("reset.html", state = "1")


#######################################################################################
@app.route("/book", methods=["GET", "POST"])
def read():
    session["book_id"] = None
    if request.method == "POST":
        session["book_id"] = request.form.get("book_id")
    r_book = Book()
    read = r_book.open()
    if session.get("user"):
        Shelf.add_book(session["book_id"])
        progress = r_book.progress()
        tools = Custom.show()
        word = Book.mean(read[1])
        return render_template("book.html", read = read, tools = tools, word = word, progress = progress, state = "True")
    return render_template("book.html", read = read, state = "False")


@app.route("/logout", methods = ["GET","POST"])
def logout():
    session["username"] = None
    session["email"] = None
    session["password"] = None
    session["user"] = None
    session["book_id"] = None
    return redirect("/")


@app.route("/close", methods = ["POST"])
def close():
    if session.get("user") and session.get("book_id"):
        progress = request.form.get("progress")
        Book.set_progress(progress)
    return redirect("/myshelf")

@app.route("/myshelf", methods = ["GET", "POST"])
def myshelf():
    if session.get("user"):
        mybooks = Shelf.show()
        return render_template("myshelf.html", mybooks = mybooks)
    return redirect("/")

@app.route("/custom", methods = ["POST"])
def custom():
    if request.form.get("fontsize"):
        Custom.set_font_size(request.form.get("fontsize"))
    if request.form.get("pagecolor"):
        Custom.set_page_color(request.form.get("pagecolor"))
    if request.form.get("textcolor"):
        Custom.set_text_color(request.form.get("textcolor"))
    return redirect("/book")


@app.route("/add", methods = ["POST"])
def add():
    if session.get("user"):
        b_id = request.form.get("book_id")
        Shelf.add_book(b_id)
        return redirect("/myshelf")
    return redirect("/")


@app.route("/remove", methods = ["POST"])
def remove():
    if session.get("user"):
        b_id = request.form.get("book_id")
        Shelf.rm_book(b_id)
        return redirect("/myshelf")
    return redirect("/")


#############################################################################
