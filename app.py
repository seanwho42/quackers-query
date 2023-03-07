import uuid
import os
import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


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
    date_up = db.Column(db.DateTime)  # date duck was placed according to the server (seems to be PST?)
    date_down = db.Column(db.DateTime)  # calculate within the app or deal with later?
    duration = db.Column(db.Interval)  # time interval duck was up.. include or calculate later?

class Response(db.Model):
    response_id = db.Column(db.String(36), primary_key=True)
    duck_id = db.Column(db.String(36))
    # could be fun to make the rating a sliding scale for input??
    rating = db.Column(db.Float)  # todo set restrictions for rating range
    same_pos = db.Column(db.Boolean)  # did they find the duck where we put it?
    moved = db.Column(db.Boolean)  # did they move the duck?
    response_time = db.Column(db.DateTime)  # time on the server the response was submitted (seems to be PST?)

@app.route('/')
def debug_index():
    return render_template('index.html')

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
    duck = db.session.execute(db.select(Duck).where(Duck.duck_id == duck_id)).scalar()
    building, floor = duck.building, duck.floor

    # todo add in whether or not they took the duck home to the form
    return render_template('form.html', duck_id=duck_id, building=building, floor=floor)


@app.route('/submit', methods=['POST'])
def submit():
    # assigning local vars to pass on individual response
    response_id = str(uuid.uuid4())
    duck_id = request.args.get('duck_id')
    rating = request.form['rating']
    if request.form['same_pos'] == 'T':
        same_pos = True
    elif request.form['same_pos'] == 'F':
        same_pos = False
    if request.form['moved'] == 'T':
        moved = True
    elif request.form['moved'] == 'F':
        moved = False
    response_time = datetime.now()  # seems to be PST? may be different on production server
    form_data = Response(response_id=response_id,
                         duck_id=duck_id,
                         rating=rating,
                         same_pos=same_pos,
                         moved=moved,
                         response_time=response_time)
    db.session.add(form_data)
    db.session.commit()
    return render_template('submit.html')  # (hopefully)

@app.route('/response-list')
def response_list():
    responses = db.session.execute(db.select(Response)).scalars()
    return render_template('response-list.html', responses=responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)