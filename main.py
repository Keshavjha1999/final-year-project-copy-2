from re import L
from django.shortcuts import render
from flask import Flask, render_template, redirect, request, flash, url_for, session, send_from_directory
from flask_cors import CORS
import os
import os.path
from werkzeug.security import generate_password_hash, check_password_hash
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='4d05b1bf662540e38cdcb3f04920577f')
# &category=sports&country=in
import sqlite3
import requests
from getRecipes import getSearchResults, getRecipeDetails
import random
app = Flask(__name__, static_folder="./static/")
app.config["SECRET_KEY"] = "mysecretkey_is_safe"
BASE_DIR = os.getcwd()
db_path = f"{BASE_DIR}/static/static/user.db"
topics = ['World', 'Nation', 'Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']


def getTopNewsBBC(top):
    url = "https://newsdata.io/api/1/news?apikey=pub_6815be6a7b827d46e97ae53a029593da3aea&language=en"
    resultnews = ""
    if(top=='World'):
        # result = newsapi.get_top_headlines(language='en', page=1, page_size=6)
        resultnews = (requests.get(url)).json()
    elif(top=='Nation'):
        result = (requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=4d05b1bf662540e38cdcb3f04920577f')).json()
        resultnews = (requests.get(url+'&country=in')).json()
    elif(top=='Business'):
        result = newsapi.get_top_headlines(language='en', category='business')
        resultnews = (requests.get(url+'&category=business')).json()
    elif(top=='Technology'):
        result = newsapi.get_top_headlines(language='en', category='technology')
        resultnews = (requests.get(url+'&category=technology')).json()
    elif(top=='Entertainment'):
        result = newsapi.get_top_headlines(language='en', category='entertainment')
        resultnews = (requests.get(url+'&category=entertainment')).json()
    elif(top=='Sports'):
        result = newsapi.get_top_headlines(language='en', category='sports')
        resultnews = (requests.get(url+'&category=sports')).json()
    elif(top=='Science'):
        result = newsapi.get_top_headlines(language='en', category='science')
        resultnews = (requests.get(url+'&category=science')).json()
    elif(top=='Health'):
        result = newsapi.get_top_headlines(language='en', category='health')
        resultnews = (requests.get(url+'&category=health')).json()
    
    images = []
    headline = []
    summary = []
    strin = []
    for a in resultnews['results']:
        contents = ""
        if 'full_description' in a:
            contents = 'full_description'
        elif 'full_description' not in a and a['content'] != None:
            contents = 'content'
        else:
            contents = 'description'
        
        if(a['image_url'] != None and a['description'] != None):
        # if(a['description'] != None):
            url = a['link']
            urlToImage = str(a['image_url'])
            headlin = str(a['title'])
            content = str(a['description'])
            if(len(content) > 140):
                content = str(content[:140]) + '...'
            urlId = url.split('/')[-1]
            if(urlId==""):
                urlId = str(random.randint(0, 1500000))
            strin.append(url + '||' + urlToImage + '||' + headlin + '||' + content + '||' + a[contents] + '||' + top + '||' + urlId +'\n')
    
    if os.path.exists("./static/myfile.txt"):
        os.remove("./static/myfile.txt")
    try:
        file1 = open("./static/myfile.txt","w", encoding='utf-8')
        file1.writelines(strin)
    except UnicodeDecodeError:
        pass

@app.route("/")
def homeScreen():
    if "user" in session:
        return render_template("home.html", username=session["user"])
    else:
        return render_template("welcome_page.html")

@app.route("/home")
def home():
    if "user" in session:
        return render_template("home.html", username=session["user"])
    else:
        return redirect(url_for("login"))

# @ app.route("/welcome")
# def welcome():
#     return render_template("welcome_page.html")

# @app.route("/bhag")
# def log():
#     return render_template("login.html")


@ app.route("/news/<top>")
def news(top):
    getTopNewsBBC(top)
    file1 = open('./static/myfile.txt', "r", encoding='utf-8')
    Lines = file1.readlines()
    url = []
    imgUrl = []
    heading = []
    content = []
    id = []
    for line in Lines:
        lin = line.split('||')
        if(len(lin)!=7):
            continue
        url.append(lin[0])
        imgUrl.append(lin[1])
        heading.append(lin[2])
        content.append(lin[3])
        top = lin[5]
        id.append(lin[6])
    file1.close()
    # print(newdict)
    if "user" in session:
        # print(session["user"])
        return render_template(
            "dataNews.html",
            username=session["user"],
            # data=news_list,
            url = url,
            imgUrl = imgUrl,
            heading = heading,
            content = content,
            data2=topics,
            top = top,
            id = id)
    else:
        return redirect(url_for("login"))
    # return render_template("news.html", data=news_list, data2=topics)
    
@ app.route("/news/<top>/<id>")
def particularNews(top, id):
    file1 = open('./static/myfile.txt', "r", encoding='utf-8')
    Lines = file1.readlines()
    url = []
    imgUrl = []
    heading = []
    contents = []
    urlId = []
    for line in Lines:
        lin = line.split('||')
        if(len(lin)!=7):
            continue
        url.append(lin[0])
        imgUrl.append(lin[1])
        heading.append(lin[2])
        contents.append(lin[4])
        urlId.append(lin[6])
    file1.close()
    ur = ""
    imgUr = ""
    head = ""
    conten = ""
    for i in range(len(url)):
        if(id == urlId[i][:-1]):
            ur = url[i]
            imgUr = imgUrl[i]
            head = heading[i]
            conten = contents[i]
            print("Found")
            break
        else:
            pass
    return render_template('single-page.html', url = ur, imgUrl = imgUr, heading = head, content = conten)
    

@ app.route("/Text-To-Speech")
def textToSpeech():
    if "user" in session:
        # print(session["user"])
        return render_template("TextToSpeech1.html", username=session["user"])
    else:
        return redirect(url_for("login"))
    # return render_template("TextToSpeech1.html")

@ app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        session.pop("user", None)
    if request.method == "POST":
        if request.form["CheckLogReg"] == "register":
            RegisterUserName = request.form["RegisterUserName"]
            RegisterPassword = generate_password_hash(
                request.form["RegisterPassword"])
            conn = sqlite3.connect(db_path)
            db = conn.cursor()
            try:
                db.execute(f"INSERT INTO login ('username', 'password') values('{RegisterUserName}','{RegisterPassword}')")
                conn.commit()
                conn.close()
            except sqlite3.IntegrityError:
                render_template("login.html", data="fail", msg="You already have an account")
            # print(RegisterUserName)
            # print(RegisterPassword)
        elif request.form["CheckLogReg"] == "login":
            conn = sqlite3.connect(db_path)
            db = conn.cursor()
            LoginUserName = request.form["LoginUserName"]
            # LoginPassWord = request.form["LoginPassword"]
            password = db.execute(
                f"SELECT password from login WHERE username = '{LoginUserName}'"
            )
            hashPass = password.fetchone()[0]
            if check_password_hash(hashPass, request.form["LoginPassword"]):
                session["user"] = LoginUserName
                # return render_template("home.html")
                return redirect(url_for("home"))
            else:
                return render_template("login.html", data="fail", msg="Incorrect Password")
            conn.close()
        else:
            return render_template("404.html")
    return render_template("login.html")


@app.route('/recipes', methods=["GET", "POST"])
def recipes():
    # dish_names = []
    if "user" in session:
        data = {'titles': [], 'prepTime': [],
                'cookTime': [], 'servings': [], 'links': []}
        if request.method == "POST" and request.form.get("searching") == "search":
            recipename = request.form.get("recipe_search")
            print(recipename)
            # module = RecipeModule(recipename)
            module = getSearchResults(recipename)
            dish_names = module.returnTitles()
            prepTime, cookTime, servings = module.returnTitleDetails()
            links = module.returnLinks()
            data = {'titles': dish_names, 'prepTime': prepTime,
                    'cookTime': cookTime, 'servings': servings, 'links': links}
            # for links in data['links']:
        else:
            print("didnt work")
        return render_template("recipes.html", username=session["user"], data=data)

    else:
        return redirect(url_for("login"))


@app.route("/recipes/<name>")
def displayRecipe(name):
    print("print link: ", name)
    data = {}
    module = getSearchResults(name)
    links = module.returnLinks()[:1]
    module2 = getRecipeDetails(links[0])
    data['title'] = name
    data['link'] = links[0]
    data['procedure'] = module2.returnProcedure()
    data['ingredients'] = module2.returnIngredients()
    data['chef'] = module2.returnChef()
    data['servings'] = module2.returnServings()
    data['preptime'] = module2.returnPrepTime()
    data['cooktime'] = module2.returnCookingTime()
    return render_template("displayrecipes.html", data=data, username=session["user"])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico')
if __name__ == "__main__":
    app.run(debug=True, port=5000)
