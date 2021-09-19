#でコメント

# from re import A
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import codecs


app = Flask(__name__)

# データベース
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = sqlalchemy.create_engine('sqlite:///sample.db', echo=True)
session = sessionmaker(bind=engine)()
#SQLAlchemyでデータベース定義
db = SQLAlchemy(app)

#SQLiteのDBテーブル情報
class BousaiItem(db.Model):
    __tablename__="bousaiitem"
    id = db.Column(Integer, primary_key=True)
    category = db.Column(String(100), nullable=False)
    name = db.Column(String(100), nullable=False)
    number = db.Column(Integer, nullable=False)
    # limit = db.Column(DateTime)

#DBの作成
db.create_all()

#備蓄一覧の表示と分岐
@app.route('/')
def bitikuitiran():
    BousaiItem_infos = db.session.query(BousaiItem.id, BousaiItem.category, BousaiItem.name, BousaiItem.number).all()
    return render_template('bitikuitiran.html', BousaiItem_infos=BousaiItem_infos)

#備蓄追加画面への分岐
@app.route('/tuika')
def bitikutuika():
    return render_template('bitikutuika.html')

#追加画面プラス書き込みのテスト
@app.route('/kakikomi',methods=['POST', 'GET'])
def bitikukakikomi():
    if request.method == 'POST':
        category = request.form['genre']
        name = request.form['name']
        number = request.form['number']
        # limit = request.form['limit']
        flask = BousaiItem(category = category, name = name, number = number)
        # ,limit = limit)
        db.session.add(flask)
        db.session.commit()
        db.session.close()
        BousaiItem_infos = db.session.query(BousaiItem.id, BousaiItem.category, BousaiItem.name, BousaiItem.number).all()
        # , BousaiItem.limit
        return render_template('kakikomi.html', BousaiItem_infos = BousaiItem_infos)
    
#備蓄品の詳細
@app.route('/detail/<int:id>')
def detail(id):
    details = db.session.query(BousaiItem).get(id)
    return render_template('detail.html', details=details)

#備蓄品の編集
@app.route('/detail/hensyu/<int:id>', methods=['GET'])
def hensyu(id):
    hensyus = db.session.query(BousaiItem).get(id)
    return render_template('hensyu.html', hensyus=hensyus)

#編集完了画面
@app.route('/detail/hensyu/<int:id>', methods=['POST'])
def finish(id):
    finishs = db.session.query(BousaiItem).get(id)
    finishs.category = request.form['genre_h']
    finishs.name = request.form['name_h']
    finishs.number = request.form['number_h']
    db.session.commit()
    db.session.close()
    finishs_after = db.session.query(BousaiItem).get(id)
    return render_template('hensyu.html', finishs_after=finishs_after, finishs=finishs) 
    # f'カテゴリーを{finishs.category}、名前を{finishs.name}、数量を{finishs.number}に変更しました。'

#マップへの分岐
@app.route('/map')
def map():
    return render_template('bousaimap.html')

#防災ニュースへの分岐
@app.route('/news')
def news():
    return render_template('bousainews.html')

#防災リンクへの分岐
@app.route('/link')
def link():
    return render_template('bousailink.html')


user_a = db.session.query(BousaiItem).all()
print(user_a)

if __name__ == '__main__':
    app.run()