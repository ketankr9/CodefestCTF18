from flask import Flask, session
from flask import render_template
import random
import string
from waitress import serve

app = Flask(__name__, static_url_path = '')
app.secret_key = '\x0f2\xaer\xffH\xba;mA\x14\xcbB\xa6\xe0#\xbe\xf5\t\xc1\xd5\xf5Dm'
problemStatement = "It is expected to complete reading a book/novel to pass the course, but the students being clever avoid reading the whole book by going through the summary only." + "Santosh(their course teacher) comes up with a new idea, he creates a magic book (you can only go to next page, that is: you can't go to next page without reading the previous one and so on, and you can only start from the beginning)" + "It is know that the flag is hidden somewhere in the book, so the only way to pass the course is to read the whole book find the flag and submit. The book has 1000 pages so better be fast. And if you are lucky you may even find the key on the very first page itself."
mTotalPages = 1000

def generateUserId(mLength):
    rand = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(mLength)])
    return rand

@app.route('/fp/')
def index_page():
    global problemStatement
    session["user"] = generateUserId(32)
    session["count"] = 0
    session["luck"] = random.randint(mTotalPages-100,mTotalPages)
    session["next_page"] = generateUserId(10)
    DATA = {"next_page": session["next_page"], 'message': problemStatement}
    return render_template('index.html', data = DATA)
    # return "user: " + session["user"]

@app.route('/np/<page_id>/')
def next_page(page_id):
    DATA = {"next_page": "", "message":" ".join([generateUserId(random.randint(1,30)) for _ in range(random.randint(100,150))])}
    session["count"] += 1
    
    if session["count"] > mTotalPages:
        return "The End, Looks like you completed the book and still haven't found the what you were looking for :("
    
    if page_id != session["next_page"]:
        return "Not Allowed!!!"
    
    if session["count"] == session["luck"]:
        DATA["message"] += " the flag is bAs!c_ScripTing&isn!t(it)"
    
    session["next_page"] = generateUserId(10)
    DATA["next_page"]=session["next_page"]
    return render_template('index.html', data = DATA)

if __name__ == "__main__":
    serve(app, listen='*:8083')
