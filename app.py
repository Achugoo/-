from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
import pymongo
from pymongo.mongo_client import MongoClient

#Database
uri = "mongodb+srv://root:root123456@cluster0.6oy0j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client.member_system
print("資料庫連線成功")


#建立Application物件 ，同時設定靜態檔案的路徑
app=Flask(
    __name__,
    static_folder = "public",   #靜態檔案資料夾
    static_url_path = "/" #靜態檔案對應的網址 
) 

#session密鑰
app.secret_key = "password"



@app.route("/")
def index():
    return render_template("index.html")

#會員網頁
@app.route("/member")
def member():
    #檢測登入狀態
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")
    
#會員註冊成功
@app.route("/member_successful")
def member_successul():
    return render_template("member_successful.html")
    
#錯誤頁面
@app.route("/error")
def error():
    msg = request.args.get("msg","發生錯誤")
    return render_template("error.html",message = msg)

#註冊頁面
@app.route("/signup",methods = ["POST"])
def signup():
    #接收前端資料
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    
    #和資料庫互動
    collection = db.user

    result = collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已註冊過QQQQ")
    
    collection.insert_one({
        "nickname":name,
        "email":email,
        "password":password
    })
    

    return redirect("/member_successful")

#登出頁面
@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")

#登入頁面
@app.route("/signin",methods = ["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]
    collection = db.user

    result = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })

    if result == None:
        return redirect("/error?msg=帳號或密碼有誤")
    session["nickname"] = result["nickname"]
    return redirect("/member")

#啟動網站伺服器,　可透過port參數指定戶號
app.run(port = 3000)

