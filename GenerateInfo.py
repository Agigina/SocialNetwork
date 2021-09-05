'''
通过随机函数，产生人的数据以及社交网络数据
'''
import random
import requests
import json
import pandas as pd
 
# 生成姓名性别
def random_name():
    # 删减部分","比较大众化姓氏
    firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
                "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
                "龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
    # 百家姓全部姓氏
    # firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平" \
    #             "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董粱杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮" \
    #             "龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴欎胥能苍" \
    #             "双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空" \
    #             "曾毋沙乜养鞠须丰巢关蒯相查後荆红游竺权逯盖益桓公晋楚闫法汝鄢涂钦归海帅缑亢况后有琴梁丘左丘商牟佘佴伯赏南宫墨哈谯笪年爱阳佟言福百家姓终"
    # 百家姓中双姓氏
    firstName2="万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫南宫"
    # 女孩名字
    girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
    # 男孩名字
    boy = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
    # 名
    name = '中笑贝凯歌易仁器义礼智信友都卡九安加金钰玉忠天'
    # 10%的机遇生成双数姓氏
    if random.choice(range(100))>10:
        firstName_name =firstName[random.choice(range(len(firstName)))]
    else:
        i = random.choice(range(int(len(firstName2)/2)))
        firstName_name =firstName2[i*2-2:i*2]
 
    sex = random.choice(range(2))
    name_1 = ""
    # 生成并返回一个名字
    if sex > 0:
        girl_name = girl[random.choice(range(len(girl)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + girl_name,"女"
    else:
        boy_name = boy[random.choice(range(len(boy)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + boy_name,"男"

# 生成地区
def random_district():
    # root="山西省阳泉市"
    dist=["城区","矿区","平定县","郊区"]
    return dist[random.randint(0,len(dist)-1)]

# 生成教育经历，小学初中高中大学
def random_education(dist):
    xiao={"城区":["新华","实验","上站","下站"],"郊区":["育才","英才","附小"],"矿区":["洪城河","二矿","三矿","四矿"],"平定县":["桃河","志华","熊猫"]}
    chu={"城区":["三中","六中","七中","实验中学","四中","二中"],"郊区":["郊区一中","郊区二中","荫营中学"],"矿区":["十一中","十五中","四矿中学","三矿中学","二矿中学"],"平定县":["平定三中","平定二中"]}
    gao=["一中","二中","三中","十一中","十五中","平定一中","郊区一中"]
    univer=["清华大学","北京大学","厦门大学","中国科学技术大学","南京大学","复旦大学","天津大学","浙江大学","西安交通大学","东南大学","上海交通大学","山东大学","中国人民大学","吉林大学","电子科技大学","四川大学","华南理工大学","兰州大学","西北工业大学","同济大学","哈尔滨工业大学","南开大学","华中科技大学","武汉大学","中国海洋大学","湖南大学","北京理工大学","重庆大学","大连理工大学","中山大学","北京航空航天大学","东北大学","北京师范大学","中南大学"]
    return xiao[dist][random.randint(0,len(xiao[dist])-1)]+"小学",chu[dist][random.randint(0,len(chu[dist])-1)],gao[random.randint(0,len(gao)-1)],univer[random.randint(0,len(univer)-1)]
# 
# 生成年龄
def random_age():
    return random.randint(18,22)

def random_hobby():
    hobby={"运动类":["篮球","羽毛球","兵乓球","足球","滑板","滑旱冰","跑步","跳绳","举重"],
    "文艺类":["听音乐","看电影","绘画","写小说","看书"],
    "智力类":["拼图","拆装积木"],
    "收藏类":["收藏扑克牌","集邮","收藏手表","收藏小汽车","收藏卡牌","收藏信封","收藏书签","收藏笔"],
    "乐器类":["弹吉他","钢琴","萨克斯","葫芦丝","大号","小号","小提琴","笛子","吹箫"],
    "文艺类":["折纸","剪纸","品茶","涂鸦","插画","绘画","读书","唱歌","舞蹈","音乐剧","舞蹈剧","戏剧","歌剧"],
    "网游":["英雄联盟","王者荣耀","刺激战场","明日方舟","和平精英","apex","怪猎","csgo","人类一败涂地","永劫无间","冬日计划"]
    }

    hobbys=[]
    sors=["运动类","文艺类","智力类","收藏类","乐器类","文艺类","网游"]
    num=random.randint(1,3)
    for i in range(num):
        ran=random.randint(0,len(sors)-1)
        hobbys.append(hobby[sors[ran]][random.randint(0,len(hobby[sors[ran]])-1)])
    return hobbys

def generate(num):
    # 写一个csv存储所有信息
    # 写一个json存储节点信息
    name=[]
    sex=[]
    xiao,chu,gao,univer=[],[],[],[]
    age=[]
    hobby1,hobby2,hobby3=[],[],[]
    mid=[]
    avatars=[]
    dist=[]
    root="山西省阳泉市"

    for uid in range(440885745,440885745+num):
        if (uid-440885745)%50==0:
            print(uid-440885745)
        url="https://tenapi.cn/bilibili/?uid="+str(uid)
        r = requests.get(url)
        mid.append(uid)
        data=json.loads(r.text)
        try:
            url=data['data']['avatar']
        except KeyError:
            url="https://c-ssl.duitang.com/uploads/blog/202106/01/20210601102818_85059.jpg"
        avatars.append(url)
            # avatars.append()
        # finally:
        #     print(r.text,uid)
        nam,se=random_name()
        name.append(nam)
        sex.append(se)
        dist1=random_district()
        dist.append(root+dist1)
        edu=random_education(dist1)
        xiao.append(edu[0])
        chu.append(edu[1])
        gao.append(edu[2])
        univer.append(edu[3])
        age.append(random_age())
        hobbies=random_hobby()
        hobby1.append(hobbies[0])
        if len(hobbies)>1:
            hobby2.append(hobbies[1])
        else:
            hobby2.append("")
        if len(hobbies)>2:
            hobby3.append(hobbies[2])
        else:
            hobby3.append("")

    dataframe = pd.DataFrame({'name':name,'sex':sex,'xiao':xiao,'chu':chu,'gao':gao,
    'univer':univer,'age':age,'hobby1':hobby1,'hobby2':hobby2,'hobby3':hobby3,
    'mid':mid,'avatars':avatars,'dist':dist})
    dataframe.to_csv("train.csv",index=False)
 
def generate_relation(num):
    # csvframe = pd.read_csv(dir)
    # print(csvframe)
    # print(csvframe.iloc[2])
    # 先整个邻接表
    # print(11)
    a=[[0 for i in range(num)] for j in range(num)]
    for item in a:
        i=random.randint(1,min(18,num))
        for j in range(i):
            ran_rela=random.randint(0,num-1)
            item[ran_rela]=1

    for i in range(num):
        for j in range(num):
            if a[i][j]!=0 and a[j][i]==0:
                a[j][i]=1
            if a[i][j]==0 and a[j][i]!=0:
                a[i][j]=1

    files=open("relation.txt",'w')
    print(num,file=files)
    for item in a:
        for n in item:
            print(n,end=" ",file=files)
        print("",file=files)
    
    files.close()

def generate_json():
    arr=[]
    nodes, links, categories=[],[],[]
    # files=open("relation.txt",'r')
    num=0
    a=[]

    # 先读入邻接矩阵
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
    
    for i in range(num):
        for j in range(num):
            if a[i][j]!=0 and a[j][i]!=0:
                a[j][i]=0
# 先整nodes表
    random_cate="abcdefghijklmnopqrstuvwxyz"
    symbolsize=[0 for i in range(num)]
    for i in range(num):
        for j in range(num):
            if a[i][j]!=0:
                symbolsize[i]+=1
                symbolsize[j]+=1

    # firstName[random.choice(range(len(firstName)))]
    csvframe = pd.read_csv("train.csv")
    for i in range(num):
        dic={}
        dic['name']=csvframe.iloc[i]['name']
        dic["symbolSize"]=symbolsize[i]
        dic["draggable"]="False"
        dic["value"]=symbolsize[i]
        dic["symbol"]="image://"+csvframe.iloc[i]["avatars"]
        dic["category"]=random_cate[random.choice(range(len(random_cate)))]
        dic["label"]={
            "normal":{
                "show":"True"
            }
        }
        nodes.append(dic)
    # print()
    # csvframe.close()
# 然后整link表
    for i in range(num):
        for j in range(num):
            if a[i][j]!=0:
                dic={}
                dic["source"]=csvframe.iloc[i]['name']
                dic["target"]=csvframe.iloc[j]['name']
                links.append(dic)
# 顶点表
    for i in range(26):
        dic={}
        dic["name"]=random_cate[i]
        categories.append(dic)

    arr.append(nodes)
    arr.append(links)
    arr.append(categories)

    json_data=json.dumps(arr)
    files=open("data.json",'w')
    print(json_data,file=files)