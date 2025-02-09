from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyAR8D8j7aogR1qKKW-kVwZ7foB814EWcMs",
  "authDomain": "auth-lab-d9cef.firebaseapp.com",
  "projectId": "auth-lab-d9cef",
  "storageBucket": "auth-lab-d9cef.appspot.com",
  "messagingSenderId": "885174428012",
  "appId": "1:885174428012:web:84508b430ced723ab39349",
  "measurementId": "G-D7W953XLY2",
  "databaseURL": "https://auth-lab-d9cef-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    return render_template("signin.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try: 
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('signup'))
        except: 
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        try: 
            login_session['user'] = auth.create_user_with_email_and_password(email , password)
            user = {'username' : request.form['username'] , "full_name": request.form['full_name'] , "bio": request.form['bio']}
            db.child("users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))  

        except: 
   
            error = "Authentication failed"
    return render_template("signup.html")

        # return render_template('signup.html')

@app.route('/add_tweet', methods=['GET','POST'])
def add_tweet():
    try:
        tweet = {"title":request.form['title'], "text":request.form ['text'], 'uid':login_session['user']['localId']}
        db.child("tweets").push(tweet)
        return render_template("tweets.html")
    except:
        print('error')
        return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET' , 'POST'])
def all_tweets():
    tweets = db.child("tweets").get().val()
    return render_template('tweets.html')








if __name__ == '__main__':
    app.run(debug=True)