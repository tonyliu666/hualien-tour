# import string
from flask import Flask,render_template,request,redirect,url_for,flash 
# from PIL import Image 
from flask_sqlalchemy import SQLAlchemy
import os,sys
import re 
from Crawler import crawl
from Crawler import selenium,store,fig_store
from send_email import SendEmail,Value
app = Flask(__name__, template_folder='templates')
base_dir = app.root_path
db_path = os.path.join(base_dir,"sqlite.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model): 
    __tablename__ = 'image'
    # _id = db.Column("id",db.Integer, primary_key=True)
    _id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    imglink = db.Column(db.String(100),nullable=False)
    loc =  db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<User %r>' % self._id
    def __init__ (self,link,title,imglink,loc):
        self.link = link
        self.title = title
        self.imglink = imglink
        self.loc = loc

def Init():
    # 卓溪鄉
    D1=Todo('scenery762.html', '瓦拉米古道', 'https://photo.travelking.com.tw/scenery/8FC68829-0DA2-4FEE-AF13-998CD0DFC2DD_d.jpg', '卓溪鄉')
    D2=Todo('scenery103296.html', '玉山國家公園', 'https://photo.travelking.com.tw/scenery/6FD2C1D6-7624-4C8D-8A76-C8644EF91E98_d.jpg', '卓溪鄉')
    D3=Todo('scenery103090.html', '南安遊客中心', 'https://photo.travelking.com.tw/scenery/E471D935-EB5B-4873-AC28-74B998475143_d.jpg', '卓溪鄉')
    D4=Todo('scenery739.html', '南安瀑布', 'https://photo.travelking.com.tw/scenery/03D922F9-4D83-46E3-9A9E-C56C540E2CAB_d.jpg', '卓溪鄉')
    D5=Todo('scenery102219.html', '新康山', 'https://photo.travelking.com.tw/scenery/95BC7A08-1F43-43B9-9B4E-CC259DD9D8F2_d.jpg', '卓溪鄉')
    D = [D1, D2, D3, D4, D5]
    db.session.add_all(D)
    # 花蓮市
    H1=Todo('scenery105521.html', '太平洋3D地景公園', 'https://photo.travelking.com.tw/scenery/6EB0613B-E8B4-405F-8CAC-FE4059162DEE_d.jpg', '花蓮市')
    H2=Todo('scenery1351.html', '大禹街','https://photo.travelking.com.tw/scenery/B79CD76E-CDA0-4F9F-A9B8-C90773C4A955_d.jpg', '花蓮市')
    H3=Todo('scenery759.html', '北濱公園', 'https://photo.travelking.com.tw/scenery/AA0296E4-9876-40EE-B010-9A0140B32194_d.jpg', '花蓮市')
    H4=Todo('scenery104997.html', '台灣菸酒公司花蓮觀光酒廠', 'https://photo.travelking.com.tw/scenery/B374862B-BE1B-4BC6-AB1D-18FD1F8C7271_d.jpg', '花蓮市')
    H5=Todo('scenery105723.html', '白燈塔公園', 'https://photo.travelking.com.tw/scenery/C91B08AA-C7B5-4B39-B1D5-89052F8AC191_d.jpg', '花蓮市')
    H6=Todo('scenery1365.html', '石藝大街', 'https://photo.travelking.com.tw/scenery/548A4D38-EC55-437D-AA09-3B35F179B615_d.jpg', '花蓮市')
    H7=Todo('scenery105096.html', '自由廣場(原城垣園)', 'https://photo.travelking.com.tw/scenery/D321F6D5-72B0-440A-9D58-856444C9350F_d.jpg', '花蓮市')
    H8=Todo('scenery105084.html', '和平廣場', 'https://photo.travelking.com.tw/scenery/39DCB62E-D908-435C-A670-48F385B6D6E0_d.jpg', '花蓮市')
    H9=Todo('scenery1352.html', '延平王廟', 'https://photo.travelking.com.tw/scenery/39CC9215-DD73-407B-A7F1-D2CD9B5B40B4_d.jpg', '花蓮市')
    H10=Todo('scenery105266.html', '東大門夜市', 'https://photo.travelking.com.tw/scenery/69F8AB2E-4B07-4670-8CFA-52EF1B3A6C9C_d.jpg', '花蓮市')
    H = [H1,H2,H3,H4,H5,H6,H7,H8,H9,H10]
    db.session.add_all(H)
    #秀林鄉
    H11=Todo('scenery105505.html', '小錐麓步道', 'https://photo.travelking.com.tw/scenery/8BA1C6F0-2459-4A18-BCFB-7D3EF25E743A_d.jpg', '秀林鄉')
    H12=Todo('scenery72.html', '天祥', 'https://photo.travelking.com.tw/scenery/AA4FA024-5F58-4B9D-9229-8679B6ECCB9B_d.jpg', '秀林鄉')
    H13=Todo('scenery744.html', '九曲洞', 'https://photo.travelking.com.tw/scenery/95C4E634-3099-4237-A6F3-86EFEB1A2934_d.jpg', '秀林鄉')
    H14=Todo('scenery459.html', '太魯閣國家公園', 'https://photo.travelking.com.tw/scenery/2669A5EB-815A-41A7-AEDA-9D240F17DD1F_d.jpg', '秀林鄉')
    H15=Todo('scenery742.html', '水簾洞', 'https://photo.travelking.com.tw/scenery/A06D8724-A76A-4191-88E3-F8CFBD325BA3_d.jpg', '秀林鄉')
    #吉安鄉
    H16=Todo('scenery103093.html', '知卡宣森林公園', 'https://photo.travelking.com.tw/scenery/38FB76FB-23B2-470C-9E0D-5BB863147293_d.jpg', '吉安鄉')
    H17=Todo('scenery1324.html', '阿美文化村', 'https://photo.travelking.com.tw/scenery/C05E3CC7-3FC4-4DA9-BBAA-21ADBAC4D8CE_d.jpg', '吉安鄉')
    H18=Todo('scenery105725.html', '新天堂樂園', 'https://photo.travelking.com.tw/scenery/96614737-1BE1-4A48-8310-32CA61B1A718_d.jpg', '吉安鄉')
    H19=Todo('scenery1418.html', '鬱金香花園', 'https://photo.travelking.com.tw/scenery/EAF66192-07F6-4536-84F3-4FF21A2E4DD4_d.jpg', '吉安鄉')
    H20=Todo('scenery105722.html', '初英親水生態公園', 'https://photo.travelking.com.tw/scenery/C55746BE-A70D-4C6D-A73D-3666B263DAE4_d.jpg', '吉安鄉')
    #光復鄉
    H21=Todo('scenery105620.html', '吉利潭遊憩區', 'https://photo.travelking.com.tw/scenery/32DD4800-442E-48B6-8FD5-FF3BBAA66608_d.jpg', '光復鄉')
    H22=Todo('scenery105621.html', '拉索埃湧泉生態園區', 'https://photo.travelking.com.tw/scenery/455579FF-E809-42A7-BA42-A90953906475_d.jpg', '光復鄉')
    H23=Todo('scenery740.html', '花蓮觀光糖廠(光復糖廠)', 'https://photo.travelking.com.tw/scenery/F7A0D8B1-6375-452B-8C6D-84CB97743E80_d.jpg', '光復鄉')
    H24=Todo('scenery104635.html', '馬太鞍自行車道', 'https://photo.travelking.com.tw/scenery/30C73F84-B2E0-4645-9513-7F51BFAF3BC8_d.jpg', '光復鄉')
    H25=Todo('scenery1322.html', '馬太鞍濕地生態園區', 'https://photo.travelking.com.tw/scenery/FDE72C5F-EA59-4862-8868-6E81ED877FF0_d.jpg', '光復鄉')
    
    #玉里鎮
    H26=Todo('scenery246.html', '安通溫泉', 'https://photo.travelking.com.tw/scenery/56D9959D-F084-4003-B687-7FA02AB750D2_d.jpg', '玉里鎮')
    H27=Todo('scenery764.html', '赤科山(赤柯山)', 'https://photo.travelking.com.tw/scenery/D6722B72-E90C-4FEF-8184-5C8B59606516_d.jpg', '玉里鎮')
    H28=Todo('scenery1398.html', '協天宮', 'https://photo.travelking.com.tw/scenery/129A6A36-7166-45AB-9F54-6C533A192CC5_d.jpg', '玉里鎮')
    H29=Todo('scenery103091.html', '鐵份瀑布', 'https://photo.travelking.com.tw/scenery/B6053A1A-B761-4609-B798-E4664A856BBC_d.jpg', '玉里鎮')
    #富里鄉
    H30=Todo('scenery1101.html', '六十石山', 'https://photo.travelking.com.tw/scenery/38D8AFEF-0D67-4BE1-B230-3D50B0A24E7A_d.jpg', '富里鄉')
    H31=Todo('scenery105179.html', '富東公路(台23線)', 'https://photo.travelking.com.tw/scenery/91029FD5-DD6E-42BB-8124-37D9989A1C6B_d.jpg"', '富里鄉')
    H32=Todo('scenery105344.htmll', '羅山大魚池', 'https://photo.travelking.com.tw/scenery/CF8B4554-1E15-4CC2-A30C-7414ABA0F1E0_d.jpg', '富里鄉')
    H33=Todo('scenery104632.html', '羅山自行車道', 'ttps://photo.travelking.com.tw/scenery/398E75B0-3663-453A-B5D8-91F6FD3CDB25_d.jpg', '富里鄉')
    H34=Todo('scenery105343.html', '羅山泥火山', 'https://photo.travelking.com.tw/scenery/7FDDEAB9-4B46-49CA-9DA1-4C5C59717EA8_d.jpg', '富里鄉')
    #新城鄉
    H35=Todo('scenery736.html', '七星潭', 'ttps://photo.travelking.com.tw/scenery/8CA7BF36-70F0-43B8-8E71-3276C83F4730_d.jpg', '新城鄉')
    H36=Todo('scenery1375.html', '光隆育樂世界', 'https://photo.travelking.com.tw/scenery/958DDEAE-17F6-42F5-844F-47A425B5F988_d.jpg', '新城鄉')
    H37=Todo('scenery105403.html', '兩潭自行車道', 'https://photo.travelking.com.tw/scenery/E4866F77-E578-4CB9-B1B0-FFA09F9D1850_d.jpg', '新城鄉')
    H38=Todo('scenery1373.html', '原野牧場', 'https://photo.travelking.com.tw/scenery/D80C4D47-A9BD-48C9-B1A4-8CCAA2E912FC_d.jpg', '新城鄉')
    H39=Todo('scenery105713.html', '新城老街', 'https://photo.travelking.com.tw/scenery/805B3AEF-6E5C-4CA4-B53B-B26BB1ADAE7D_d.jpg', '新城鄉')
    #瑞穗鄉
    empty = [H11,H12,H13,H14,H15,H16,H17,H18,H19,H20,H21,H22,H23,H24,H25,H26,H27,H28,H29,H30,H31,H32,H33,H34,H35,H36,H37,H38,H39]
    db.session.add_all(empty)
    H39=Todo('scenery750.html', '秀姑巒溪', 'https://photo.travelking.com.tw/scenery/3C2243A9-DDE9-41C7-BE31-157B7981AE5D_d.jpg', '瑞穗鄉')
    H40=Todo('scenery105415.html', '吉蒸牧場', 'https://photo.travelking.com.tw/scenery/D8916707-0E72-462D-AC33-0F043CDE519E_d.jpg', '瑞穗鄉')
    H41=Todo('scenery1382.html', '虎頭山', 'https://photo.travelking.com.tw/scenery/6410A7FF-F074-4C20-A424-254B9E5286FE_d.jpg', '瑞穗鄉')
    H42=Todo('scenery98.html', '富源國家森林遊樂區', 'https://photo.travelking.com.tw/scenery/47B00525-E442-4282-9750-F636534B1EA9_d.jpg', '瑞穗鄉')
    H43=Todo('scenery1376.html', '瑞穗牧場', 'https://photo.travelking.com.tw/scenery/2920E605-15D0-430C-9DAC-6E6B96AECF18_d.jpg', '瑞穗鄉')
    #萬榮鄉
    H44=Todo('scenery103087.html', '七彩湖', 'https://photo.travelking.com.tw/scenery/7C39A5FD-93F4-4E1D-B469-3760B3631682_d.jpg', '萬榮鄉')
    H45=Todo('scenery746.html', '花蓮紅葉溫泉', 'https://photo.travelking.com.tw/scenery/5CC77ACE-DA92-44AB-88DE-23C66F7C3AFB_d.jpg', '萬榮鄉')
    #壽豐鄉
    H45=Todo('scenery731.html', '牛山', 'https://photo.travelking.com.tw/scenery/526A5379-06A1-47C6-B072-6A0499E13456_d.jpg', '壽豐鄉')
    H47=Todo('scenery105508.html', '白鮑溪自行車道', 'https://photo.travelking.com.tw/scenery/B779533D-D828-4703-B2EB-3ECB291A8553_d.jpg', '壽豐鄉')
    H48=Todo('scenery102.html', '池南國家森林遊樂區', 'https://photo.travelking.com.tw/scenery/C2AF2424-277F-46CD-A2A7-DD623D1F1A37_d.jpg', '壽豐鄉')
    H49=Todo('scenery1389.html', '東華大學', 'https://photo.travelking.com.tw/scenery/412144AF-8ED4-4B97-906A-ECBF624E1C0B_d.jpg', '壽豐鄉')
    H50=Todo('scenery1157.html', '遠雄海洋公園', 'https://photo.travelking.com.tw/scenery/40AB2151-AEB7-435A-B5A2-EC0DE8EA024E_d.jpg', '壽豐鄉')
    #鳳林鎮
    H51=Todo('scenery758.html', '林田山林業文化園區', 'https://photo.travelking.com.tw/scenery/50DAAB55-214C-4519-AD0E-01148814F474_d.jpg', '鳳林鎮')
    H52=Todo('scenery105147.html', '校長夢工廠', 'https://photo.travelking.com.tw/scenery/DA847B17-559A-4556-83AF-939C9516BC7B_d.jpg', '鳳林鎮')
    H53=Todo('scenery105155.html', '菸樓文化聚落', 'https://photo.travelking.com.tw/scenery/612671F1-D388-4E45-A307-656F1EBDF88E_d.jpg', '鳳林鎮')
    H54=Todo('scenery748.html', '新光兆豐休閒農場', 'https://photo.travelking.com.tw/scenery/543F0AC8-6240-478D-B3FC-8614324AF3A0_d.jpg', '鳳林鎮')
    H55=Todo('scenery105363.html', '鳳林自行車道', 'https://photo.travelking.com.tw/scenery/A05D1C23-B031-4524-8D4B-34FE27493F96_d.jpg', '鳳林鎮')
    empty2=[H40,H41,H42,H43,H44,H45,H47,H48,H49,H50,H51,H52,H53,H54,H55]
    db.session.add_all(empty2)
    
    #豐濱鄉(明天弄)
    H56=Todo('scenery105361.html', '石門長濱自行車道', 'https://photo.travelking.com.tw/scenery/5CEF8658-FAF3-46BF-AC04-59EC8CA25072_d.jpg', '豐濱鄉')
    H57=Todo('scenery105701.html', '石門班哨角休憩區', 'https://photo.travelking.com.tw/scenery/1C133F29-0C13-40AA-B8B1-F18CD128C587_d.jpg', '豐濱鄉')
    H58=Todo('scenery101.html', '石梯坪', 'https://photo.travelking.com.tw/scenery/EA854F68-7B01-4E66-9BBC-6A113ECC0CF7_d.jpg', '豐濱鄉')
    H59=Todo('scenery1414.html', '靜浦北回歸線', 'https://photo.travelking.com.tw/scenery/5AC28A82-1A19-4651-AF64-27D3D4D00A27_d.jpg', '豐濱鄉')
    H60=Todo('scenery100.html', '豐濱月洞', 'https://photo.travelking.com.tw/scenery/DDA020E3-320E-421B-83A5-9B6076117985_d.jpg', '豐濱鄉')
    #第一次使用請使用db.session.commit()，接下來把它註解在rerun一次
    empty3 = [H56,H57,H58,H59,H60]
    db.session.add_all(empty3)
    # db.session.commit()
    
@app.route('/')
def index(): 
    return render_template('home.html')

@app.route('/Taipei',methods=["GET"])
def Taipei_navigate():
    return render_template('taipei.html')
@app.route('/Yilan',methods=["GET"])
def Yilan_navigate():
    return render_template('Yilan.html')
@app.route('/Hualien',methods=["GET","POST"])
def Hualien_navigate():
    if request.method == "POST":
        # import re
        # print(request.form.get('check'),sys.stderr)
        # if request.form.getlist('check') != None:
        #     return render_template('Hualien.html',click=True)
        # if request.form.get('OrderDay')!=None:
        
        if request.form['s'] == "確定":
            fig_store.set = True
        elif request.form['s'] == "送出":
            value = request.form.get('OrderDay')
            Value.string = value
        elif request.form['s'] == "寄出":
            url = "https://www.google.com/search?q="+"花蓮"+Value.Value_back()
            tour=crawl(url).tour_guide(url)
            Email = request.form.get('email')
            pack = [app,tour,Email]
            SendEmail(pack).send_email(pack)
        else:
            value = request.form.get('OrderDay')
            if value == "親子友善":
                url = 'https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fg%2F11clhptb5_&dest_state_type=sattd&dest_src=yts&q=%E8%8A%B1%E8%93%AE&ved=0CAAQ8IAIahcKEwj4pI2mhIT5AhUAAAAAHQAAAAAQCg&rf=Eh8KDS9nLzExYzcxaHZmdDASDOimquWtkOWPi-WWhCgB'
            elif value == "戶外活動":
                url = 'https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fg%2F11clhptb5_&dest_state_type=sattd&dest_src=yts&q=%E8%8A%B1%E8%93%AE&ved=0CAAQ8IAIahcKEwj4pI2mhIT5AhUAAAAAHQAAAAAQCg&rf=Eh8KDS9nLzExYmM1OGwxM3cSDOaItuWklua0u-WLlSgB'
            elif value == "藝術與文化":
                url ='https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fg%2F11clhptb5_&dest_state_type=sattd&dest_src=yts&q=%E8%8A%B1%E8%93%AE&ved=0CAAQ8IAIahcKEwj4pI2mhIT5AhUAAAAAHQAAAAAQCg&rf=EhwKBy9tLzBqancSD-iXneihk-iIh-aWh-WMligB'
            elif value == "歷史":
                url = 'https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fg%2F11clhptb5_&dest_state_type=sattd&dest_src=yts&q=%E8%8A%B1%E8%93%AE&ved=0CAAQ8IAIahcKEwj4pI2mhIT5AhUAAAAAHQAAAAAQCg&rf=EhQKCC9tLzAzZzN3Egbmrbflj7IoAQ'
            elif value == "海灘":
                url = 'https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F025c70&dest_state_type=main&dest_src=yts&rf=EgwKCC9tLzBiM3lyKAE&q=%E8%8A%B1%E8%93%AE%E6%B5%B7%E7%81%98&ved=0CAAQ8IAIahgKEwig1r3ChIT5AhUAAAAAHQAAAAAQnAM&tcfs=EhcKDS9nLzExY2xocHRiNV8SBuiKseiTrg'
            fig_stars = crawl(url).google_search(url)
            fig_store.fig = fig_stars
        return render_template('Hualien.html',figstars = fig_store.fig_back(),click=fig_store.set_back())       
                # redirect(url_for('Hualien_lookup',another = another))  
    else:
        return render_template('Hualien.html')
        
@app.route('/Hualien/google/<name>', methods=["GET"])
def Hualien_google(name):
    # data = Todo.query.all()
    address = "https://www.google.com/search?q="+name
    return redirect(address)


@app.route('/Hualien/spot/', methods=["GET","POST"])
def Hualien_spot():
    # data = Todo.query.all()
    data = Todo.query.filter_by(loc='花蓮市').all()
    if request.method == "POST":
        another = []
        task_content = request.form['value']
        for todo in Todo.query.all(): 
            # if todo._id > 5 : 
            if todo.title == task_content:
                another.append(todo._id)
        # print("The number is %d"%(another[0]),file=sys.stderr)
        return redirect(url_for('Hualien_lookup',another = another))
         
    else: 
        # copy_data = Todo.query.all()
        # if len(another) != 0 :
        #     return render_template('Hualien_spot.html',data = another)
        # else: 
        #     print(copy_data,file=sys.stderr)
        #     return render_template('Hualien_spot.html',data = copy_data)
        return render_template('Hualien_spot.html',data = data)


@app.route('/Hualien/spot/loc',methods=["GET","POST"])
def Hualien_lookup():
    data = []
    keys = request.args.get('another')
    ans = Todo.query.get_or_404(keys)
    data.append(ans)
    return render_template('Hualien_spot.html',data = data)
@app.route('/Hualien/hotel',methods=["GET"])
def Hualien_hotel():
    url = 'https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AED6AEBiAIBqAIDuAK7zuCWBsACAdICJDcyNDQyZWYxLWY2OTktNGJhZC1iNjEzLTE1NjM0OTFlOTg5MtgCBOACAQ&sid=80c3dd2e865839ba50f84a6b88e186fd&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.zh-tw.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AED6AEBiAIBqAIDuAK7zuCWBsACAdICJDcyNDQyZWYxLWY2OTktNGJhZC1iNjEzLTE1NjM0OTFlOTg5MtgCBOACAQ%26sid%3D80c3dd2e865839ba50f84a6b88e186fd%26sb_price_type%3Dtotal%26%26&ss=%E8%8A%B1%E8%93%AE&is_ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=%E8%8A%B1%E8%93%AE&search_pageview_id=f57570de8fad009e'
    return redirect(url)
    

##################
# 這邊是 li flag裡面的 a tag超連結設定
##################
@app.route('/Hualien/全部',methods=["GET"])
def all_lookup():
    result = Todo.query.all() #已 return全部的花蓮市景點加入進來
    return render_template('Hualien_spot.html',data = result)

@app.route('/Hualien/花蓮市',methods=["GET"])
def hualien_lookup():
    result = Todo.query.filter_by(loc='花蓮市').all() #已 return全部的花蓮市景點加入進來
    return render_template('Hualien_spot.html',data = result)

@app.route('/Hualien/玉里鎮',methods=["GET"])
def yuli_lookup():
    result = Todo.query.filter_by(loc='玉里鎮').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/光復鄉',methods=["GET"])
def kongfu_lookup():
    result = Todo.query.filter_by(loc='光復鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/吉安鄉',methods=["GET"])
def jian_lookup():
    result = Todo.query.filter_by(loc='吉安鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/秀林鄉',methods=["GET"])
def hsulin_lookup():
    result = Todo.query.filter_by(loc='秀林鄉').all()
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/富里鄉',methods=["GET"])
def fuli_lookup():
    result = Todo.query.filter_by(loc='富里鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/新城鄉',methods=["GET"])
def shinchen_lookup():
    result = Todo.query.filter_by(loc='新城鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/瑞穗鄉',methods=["GET"])
def resei_lookup():
    result = Todo.query.filter_by(loc='瑞穗鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/萬榮鄉',methods=["GET"])
def vanlung_lookup():
    result = Todo.query.filter_by(loc='萬榮鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/壽豐鄉',methods=["GET"])
def shufun_lookup():
    result = Todo.query.filter_by(loc='壽豐鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/鳳林鎮',methods=["GET"])
def vanlin_lookup():
    result = Todo.query.filter_by(loc='鳳林鎮').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/豐濱鄉',methods=["GET"])
def fungbin_lookup():
    result = Todo.query.filter_by(loc='豐濱鄉').all() 
    return render_template('Hualien_spot.html',data = result)
@app.route('/Hualien/卓溪鄉',methods=["GET"])
def jushi_lookup():
    result = Todo.query.filter_by(loc='卓溪鄉').all() 
    return render_template('Hualien_spot.html',data = result)
    
##################
# 這邊是 li flag裡面的 a tag超連結設定
##################

#各個景點介紹: 

@app.route('/<title>/<link_name>',methods=["GET"])
def plot_routing(link_name,title):
    link_name = "https://www.travelking.com.tw/tourguide/hualien/" + link_name
    data = crawl(link_name)
    data = data.data(link_name)
    data.append(title)
    data.append(len(data))
    store.List = data 
    return render_template('introduction.html',data = data,set = False)

@app.route('/booking/<variable>')
def booking(variable):
    # try:
        data = store.list_back()
        variable = re.sub('[a-zA-Z]',"",variable)
        variable = re.sub('[1-9]',"",variable)
        sel = selenium(variable).data(variable)
        # for i in sel : 
        #     sel[sel.index(i)] = f"{sel[sel.index(i)]}"
        # print(type(sel[0]),sys.stderr)
        text = "為您推薦五筆優質旅館"
        return render_template('introduction.html',data = data,sel=sel,text =text,set=True)
        # return f"{sel[0]} "
    # except:
    #     return redirect(url_for('Hualien_spot'))
if __name__ =='__main__':
    db.create_all() 
    Init()
    # app.run(host="0.0.0.0",port="1010",debug=True)
    app.run(host="0.0.0.0",port="1010",debug=True)
    # host="0.0.0.0",


