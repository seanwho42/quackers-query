import qrcode
import uuid
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import select


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Duck(db.Model):
    week_num = db.Column(db.Integer)
    building = db.Column(db.String(36))
    floor = db.Column(db.String(36))
    height = db.Column(db.String(36))
    rep_number = db.Column(db.Integer)
    duck_id = db.Column(db.String(36), primary_key=True)
    date_up = db.Column(db.DateTime)  # date placed
    date_down = db.Column(db.DateTime)  # date
    duration = db.Column(db.Interval)  # time interval duck was up.. include or calculate later?

class Response(db.Model):
    response_id = db.Column(db.String(36), primary_key=True)
    duck_id = db.Column(db.String(36))
    # could be fun to make the rating a sliding scale for input??
    rating = db.Column(db.Float)  # todo set restrictions for rating range
    moved = db.Column(db.Boolean)  # did they find the duck where we put it?


# todo update this when we implement a domain name
# todo set this up with proper ids and make it in a more printable format -- using PIL?
# todo move this to its own file since it isn't really --necessarily-- part of the web app
def generate_qr_code(duck_id):
    duck_id = str(uuid.uuid4())
    url = f'http://137.184.35.65:81/form?duck_id={duck_id}'  # todo update
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"/qr_codes/qr_code_{duck_id}.png")
    return f'<img src="qr_code_{duck_id}.png" alt="QR code">'

@app.route('/')
def debug_index():
    return '<i>Still working on this.. :)</i>'

# def index_info():
#     sql_stmt = select(FormData)
#     # todo make this a jinja template instead probably
#     responses = FormData.query.all()
#     print(responses)
#     return f'{responses}'


# def data_to_html(select_stmt):
#     """
#     takes data from a sqlalchemy select statement and makes an html list out of it
#     """
#     li_list = []
#     for row in select_stmt:
#         li_list.append(f'<li>{row}</li>')
#     return li_list

@app.route('/form')
def form():
    duck_id = request.args.get('duck_id')
    # duck = db.get_or_404(Duck, duck_id)
    # building, room = duck.building, duck.room
    return f'''
        <form method="POST" action="/submit?id={duck_id}">
            <label>Rating:</label><input type="text" name="rating"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    # assigning local vars to pass on individual response
    response_id = str(uuid.uuid4())
    duck_id = request.args.get('duck_id')
    rating = request.form['rating']
    form_data = Response(response_id=response_id, duck_id=duck_id, rating=rating)
    db.session.add(form_data)
    db.session.commit()
    return 'Form submitted successfully!'  # (hopefully)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)