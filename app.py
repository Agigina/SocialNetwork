from flask import Flask,render_template,request,flash, redirect, url_for,send_from_directory
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_login import UserMixin, LoginManager,AnonymousUserMixin,login_user, logout_user, login_required, current_user
import hashlib
import os
from pyecharts import options as opts
from pyecharts.charts import Graph
import shutil
from GenerateInfo import generate_relation,generate_json
import json
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from jinja2 import Markup
from Dijistra import Dijistra,caculate_all
import pandas as pd

app=Flask(__name__)

db=SQLAlchemy(app)

app.secret_key='password'

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:yibo83@127.0.0.1:3306/ds_assign?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

class User(UserMixin, db.Model):
    # 没有昵称，只有qq号和密码
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(128))
    email_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.get_email_hash()

    def get_email_hash(self):
        if self.email is not None and self.email_hash is None:
            self.email_hash = hashlib.md5(self.email.encode(
                'utf-8')).hexdigest()  # encode for py23 compatible

    @property
    def gravatar(self):
        if self.id <= 40:
            return 'https://gravatar.com/avatar/%s?d=monsterid' % self.email_hash
        else:
            return 'https://q4.qlogo.cn/g?b=qq&nk={qqnumber}&s=140'.format(qqnumber=self.email)

rich_text = {
    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
    "abg": {
        "backgroundColor": "#e3e3e3",
        "width": "100%",
        "align": "right",
        "height": 22,
        "borderRadius": [4, 4, 0, 0],
    },
    "hr": {
        "borderColor": "#aaa",
        "width": "100%",
        "borderWidth": 0.5,
        "height": 0,
    },
    "b": {"fontSize": 16, "lineHeight": 33},
    "per": {
        "color": "#eee",
        "backgroundColor": "#334455",
        "padding": [2, 4],
        "borderRadius": 2,
    },
}

hobby={"运动类":["篮球","羽毛球","兵乓球","足球","滑板","滑旱冰","跑步","跳绳","举重"],
    "文艺类":["听音乐","看电影","绘画","写小说","看书"],
    "智力类":["拼图","拆装积木"],
    "收藏类":["收藏扑克牌","集邮","收藏手表","收藏小汽车","收藏卡牌","收藏信封","收藏书签","收藏笔"],
    "乐器类":["弹吉他","钢琴","萨克斯","葫芦丝","大号","小号","小提琴","笛子","吹箫"],
    "文艺类":["折纸","剪纸","品茶","涂鸦","插画","绘画","读书","唱歌","舞蹈","音乐剧","舞蹈剧","戏剧","歌剧"],
    "网游":["英雄联盟","王者荣耀","刺激战场","明日方舟","和平精英","apex","怪猎","csgo","人类一败涂地","永劫无间","冬日计划"]
    }

def bar_base():
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 30, 18, 65, 70])
            .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
    )
    return bar

@app.route("/1")
def index():
    return render_template("index.html")

@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@app.route('/', methods=["GET", "POST"])
def login():
    # print("aaa")
    if request.method == "GET":
        # return render_template('calm-breeze-login-screen/dist/index.html')
        print("get")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # print(username,password)
        if not all ([username,password]):
            flash(u"参数不完整")
        return redirect(url_for('welcomes'))
        # user = User.query.filter_by(email=username).first()
        # print("ss",type(int(username)),int(username),user)
        # if user is not None:
        #     print("not none")
        #     if user.get_password(password):
        #         # login_user(user)
        #         return redirect(url_for('welcome'))
        # else:
        #     user = User(email=username, password=password)
        #     db.session.add(user)
        #     db.session.commit()
        #     # login_user(user)
        #     return redirect(url_for('welcomes'))
        
    return render_template('calm-breeze-login-screen/dist/index.html')

@app.route('/welcome')
def welcomes():
    return render_template('menu/index.html')

@app.route('/upload2', methods=["GET", "POST"])
def upload2():
    if request.method == "POST":
        f=request.files['myfiles']
        f.save(f.filename)
        print(f.filename)
        if f.filename!="relation.txt":
            shutil.copy(f.filename,"relation.txt")
        generate_json()
        with open("data.json", "r", encoding="utf-8") as f:
            j = json.load(f)
            nodes, links, categories = j
        c = (
            Graph(opts. InitOpts(width="1500px",height="600px",page_title="Display",renderer= "svg",theme="macarons"))
            .add(
                "",
                nodes,
                links,
                categories,
                repulsion=50,
                linestyle_opts=opts.LineStyleOpts(curve=0.2),
                label_opts=opts.LabelOpts(is_show=False),
                layout="force"
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
                title_opts=opts.TitleOpts(title="群体社交关系图",title_textstyle_opts=opts.TextStyleOpts(
                        color='blue',
                        font_size="30",
                        # rich=rich_text
                    ),pos_left="30%"),
                toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                orient="vertical",
                feature=opts.ToolBoxFeatureOpts(
                    # save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(type_="jpeg", icon=image://url, pixel_ratio=2),
                    restore=opts.ToolBoxFeatureRestoreOpts(),
                    data_view=opts.ToolBoxFeatureDataViewOpts(),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                    magic_type=opts.ToolBoxFeatureDataViewOpts(),
                    brush=opts.ToolBoxFeatureDataZoomOpts(),
                )
            )
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=False)
            )
            .render("../templates/graph.html")
        )
        return render_template('graph.html')
    return render_template('choices/upload/index1.html')

@app.route('/choice1', methods=["GET", "POST"])
def choice1():
    if request.method == "POST":
        f=request.files['myfiles']
        f.save(f.filename)
        print(f.filename)
        if f.filename!="train.csv":
            shutil.copy(f.filename,"train.csv")
        return redirect(url_for('upload2'))
    return render_template('choices/upload/index.html')

@app.route('/choice2', methods=["GET", "POST"])
def choice2():
    return render_template('graph.html')

@app.route('/result', methods=["GET", "POST"])
def test():
    return render_template('choices/upload/download.html')

@app.route('/download/<filename>', methods=["GET", "POST"])
def download(filename):
    return send_from_directory("",filename, as_attachment=True)

@app.route('/choice3', methods=["GET", "POST"])
def choice3():
    # 获取输入，保存成一个txt
    if request.method == "POST":
        keyvalue = request.form['keyvalue']
        with open("data.json", "r", encoding="utf-8") as f:
            j = json.load(f)
            nodes, links, categories = j
        
        link2=[]
        for item in links:
            if item["source"]!=keyvalue and item["target"]!=keyvalue:
                continue
            else:
                link2.append(item)
        
        now=[]
        node_exist=[]
        # 还得删除一下除了朋友圈之外的人
        for item in link2:
            if item["source"] not in node_exist:
                node_exist.append(item["source"])
            if item["target"] not in node_exist:
                node_exist.append(item["target"])
        
        node2=[]
        for item in nodes:
            if item["name"] in node_exist:
                node2.append(item)
        now.append(node2)
        now.append(link2)
        now.append(categories)
        json_data=json.dumps(now)
        files=open("data1.json",'w')
        print(json_data,file=files)
        files.close()
        with open("data1.json", "r", encoding="utf-8") as f:
            j = json.load(f)
            nodes, links, categories = j
        c = (
            Graph(opts. InitOpts(width="1500px",height="600px",page_title="Display",renderer= "svg",theme="macarons"))
            .add(
                "",
                nodes,
                links,
                categories,
                repulsion=50,
                linestyle_opts=opts.LineStyleOpts(curve=0.2),
                label_opts=opts.LabelOpts(is_show=False),
                layout="force"
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),
                title_opts=opts.TitleOpts(title="个人社交网络图",title_textstyle_opts=opts.TextStyleOpts(
                        color='blue',
                        font_size="30",
                        # rich=rich_text
                    ),pos_left="30%"),
                toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                orient="vertical",
                feature=opts.ToolBoxFeatureOpts(
                    # save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(type_="jpeg", icon=image://url, pixel_ratio=2),
                    restore=opts.ToolBoxFeatureRestoreOpts(),
                    data_view=opts.ToolBoxFeatureDataViewOpts(),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                    magic_type=opts.ToolBoxFeatureDataViewOpts(),
                    brush=opts.ToolBoxFeatureDataZoomOpts(),
                )
            )
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=False)
            )
            .render("../templates/graph1.html")
        )
        return render_template('graph1.html')
    # 如上
    return render_template('choices/input-box/index1.html')

@app.route('/choice4', methods=["GET", "POST"])
def choice4():
    if request.method == "POST":
        keyvalue = request.form['keyvalue']
        # 获取一下编号是哪个，从csv里
        
        with open("data.json", "r", encoding="utf-8") as f:
            j = json.load(f)
            nodes, links, categories = j
        
        link2=[]
        for item in links:
            if item["source"]!=keyvalue and item["target"]!=keyvalue:
                continue
            else:
                link2.append(item)
        
        now=[]
        node_exist=[]
        # 还得删除一下除了朋友圈之外的人
        for item in link2:
            if item["source"] not in node_exist:
                node_exist.append(item["source"])
            if item["target"] not in node_exist:
                node_exist.append(item["target"])
        
        node2=[]
        for item in nodes:
            if item["name"] in node_exist:
                node2.append(item)

        # 获取邻接矩阵
        num=0
        a=[]
        with open("relation.txt",'r') as f:
            num=int(f.readline())
            a=[[0 for i in range(num)] for j in range(num)]
            i=0
            for line in f:
                lis=line.rstrip("\n").rstrip(" ").split(" ")
                # print(lis)
                lis1=[int(float(item.rstrip("\n").rstrip(" "))) for item in lis]
                a[i]=lis1
                i+=1
            f.close()

        csvframe = pd.read_csv("train.csv")
        names=[]
        for i in range(num):
            names.append(csvframe.iloc[i]["name"])
        
        nownum=names.index(keyvalue)
        d=[]
        hobby_cate=[]
        for item in hobby:
            if csvframe.iloc[nownum]["hobby1"] in hobby[item]:
                hobby_cate.append(item)
            if type(csvframe.iloc[nownum]["hobby2"]) is str and len(csvframe.iloc[nownum]["hobby2"])!=0:
                if csvframe.iloc[nownum]["hobby2"] in hobby[item] and item not in hobby_cate:
                    hobby_cate.append(item)
            if type(csvframe.iloc[nownum]["hobby3"]) is str and len(csvframe.iloc[nownum]["hobby3"])!=0:
                if csvframe.iloc[nownum]["hobby3"] in hobby[item] and item not in hobby_cate:
                    hobby_cate.append(item)
        print(hobby_cate)
        for i in range(num):
            path, dis = Dijistra(nownum,i,a)
            # print(csvframe.iloc[i]["hobby2"])
            note=""
            if csvframe.iloc[nownum]["xiao"]==csvframe.iloc[i]["xiao"]:
                note+="同一小学 "
            if csvframe.iloc[nownum]["chu"]==csvframe.iloc[i]["chu"]:
                note+="同一初中 "
            if csvframe.iloc[nownum]["gao"]==csvframe.iloc[i]["gao"]:
                note+="同一高中 "  
            if csvframe.iloc[nownum]["univer"]==csvframe.iloc[i]["univer"]:
                note+="同一大学 "
            if csvframe.iloc[nownum]["dist"]==csvframe.iloc[i]["dist"]:
                note+="同一地区 "

            for item in hobby_cate:
                if csvframe.iloc[i]["hobby1"] in hobby[item]:
                    note+="有"+item+"共同爱好 "
                if type(csvframe.iloc[i]["hobby2"]) is str and len(csvframe.iloc[i]["hobby2"])!=0:
                    if csvframe.iloc[i]["hobby2"] in hobby[item]:
                        note+="有"+item+"共同爱好 "
                if type(csvframe.iloc[i]["hobby3"]) is str and len(csvframe.iloc[i]["hobby3"])!=0:
                    if csvframe.iloc[i]["hobby3"] in hobby[item]:
                        note+="有"+item+"共同爱好 "

            d.append([csvframe.iloc[i]["name"],csvframe.iloc[i]["dist"],
            csvframe.iloc[i]["xiao"]+","+csvframe.iloc[i]["chu"]+","+csvframe.iloc[i]["gao"]+","+csvframe.iloc[i]["univer"],
            csvframe.iloc[i]["hobby1"]+("" if type(csvframe.iloc[i]["hobby2"]) is not str or len(csvframe.iloc[i]["hobby2"])==0 else (
                ","+csvframe.iloc[i]["hobby2"]+"" if type(csvframe.iloc[i]["hobby3"]) is not str or len(csvframe.iloc[i]["hobby3"])==0 else (
                    ","+csvframe.iloc[i]["hobby3"]
                )
            )),
            # csvframe.iloc[i]["hobby1"]+len(csvframe.iloc[i]["hobby2"])==0?"":(","+
            # csvframe.iloc[i]["hobby2"]+len(csvframe.iloc[i]["hobby3"])==0?"":(","+
            # csvframe.iloc[i]["hobby3"])),
            path,note,i,dis])
        
        d=sorted(d, key=lambda a: a[-1])
        # 如果距离等于2，那么有共同好友，计算，如果小于2，那么删除，如果大于2，那么是负数
        headers='''
            <!DOCTYPE html>
            <html lang="en" >
            <head>
            <meta charset="UTF-8">
            <title>Find Possible Friends</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
            <link rel="stylesheet" href="static/css/style4.css">

            </head>
            <body>
            <!-- partial:index.partial.html -->
            <section>
            <!--for demo wrap-->
            <h1>Possible Friends</h1>
            <div class="tbl-header">
                <table cellpadding="0" cellspacing="0" border="0">
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>District</th>
                    <th>Education</th>
                    <th>Hobbies</th>
                    <th>Relationship</th>
                    <th>Notes</th>
                    </tr>
                </thead>
                </table>
            </div>
            <div class="tbl-content">
                <table cellpadding="0" cellspacing="0" border="0">
                <tbody>'''
        endings='''
                </tbody>
                </table>
            </div>
            </section>


            <!-- follow me template -->
            <div class="made-with-love">
                <i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i><i>♥</i> 
            <br>
            <br>
            
            <a href="/welcome">Return</a>
            </div>
            <!-- partial -->
            <!-- <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script><script  src="./script.js"></script> -->

            </body>
            </html>
                '''
        new_d=[]
        for item in d:
            # 好友或自己
            if item[-1]==1 or item[-1]==999:
                continue
            if item[0]==keyvalue:
                continue
            elif item[-1]==2:
                # 重新计算共同好友数
                item[-1]=caculate_all(nownum,item[-2],a)
                new_d.append(item)
            else:
                item[-1]=int(0-int(item[-1]))
                new_d.append(item)
        new_d=sorted(new_d, key=lambda a: a[-1],reverse=True)
        with open("../templates/table.html",'w',encoding='utf-8') as files:
            print(headers,file=files)
            for item in new_d:
                print("<tr>",file=files)
                print("<td>",file=files)
                print(item[0],file=files)
                print("</td>",file=files)
                print("<td>",file=files)
                print(item[1],file=files)
                print("</td>",file=files)
                print("<td>",file=files)
                print(item[2],file=files)
                print("</td>",file=files)
                print("<td>",file=files)
                print(item[3],file=files)
                print("</td>",file=files)
                print("<td>",file=files)
                print(item[-1],file=files)
                print("</td>",file=files)
                print("<td>",file=files)
                print(item[-3],file=files)
                print("</td>",file=files)
                print("</tr>",file=files)
            print(endings,file=files)
            f.close()
        return render_template('table.html')
    # 如上
    return render_template('choices/input-box/index2.html')
if __name__== "__main__":
    app.run()