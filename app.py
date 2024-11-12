from flask import Flask, render_template, request
from flask_assets import Environment, Bundle


app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")
js = Bundle("src/*.js", output="dist/main.js")

assets.register("css", css)
assets.register("js", js)

css.build()
js.build()


class User:
    id = 0
    def __init__(self, fname, lname, email ):
        User.id  += 1
        self.id = User.id 
        self.fname = fname
        self.lname = lname 
        self.email = email

    def search( self, word ):
        if (word is None):
            return False
        all = self.fname + self.lname + self.email
        return word.lower() in all.lower()

users = [
    User("abe", "vida", "abe@nowhere.com"),
    User("betty", "b", "bb@nowhere.com"),
    User("joe", "robinson", "jrobinson@nowhere.com"),

    User("Luis", "Cortes", "Luis@somewhere.com"),
    User("marty", "hinkle", "mhinkle@nowhere.com"),
    User("matthew", "robinson", "mrobinson@nowhere.com"),

    User("collin", "western", "cwest@nowhere.com"),
    User("marty", "hinkle II", "mhinkle2@nowhere.com"),
    User("joe", "robinson", "jrobinson@nowhere.com"),

    User("juan", "vida", "juanvida@nowhere.com"),
    User("marty", "hinkle III", "mhinkle3@nowhere.com"),
    User("zoe", "omega", "zoe@nowhere.com") 
]




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    word = request.form.get("search")
    if (word is None or word == ""):
        return render_template("search.html", users=[])
    else:
        return render_template("search.html", users=filter(lambda u: u.search(word), users))
    
if __name__ == "__main__":
    app.run(debug=True)
