import uuid
import os
import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


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
    # todo make this a template instead

    return f'''
        <form method="POST" action="/submit?duck_id={duck_id}">
            <label>Rating:</label><input type="text" name="rating"><br>
            <label>Did you find the duck in {building} on the {floor} floor?</label>
            <input type="radio" name="moved" id="t_radio" value="T" checked="checked"><label>
            <label for="t_radio">Yes</label>

            <input type="radio" name="moved" id="f_radio" value="F"><label>
            <label for="f_radio">No</label>

            <br>
            <input type="submit" value="Submit">
        </form>
    '''

#             <input type="checkbox" name="moved">


@app.route('/submit', methods=['POST'])
def submit():
    # assigning local vars to pass on individual response
    response_id = str(uuid.uuid4())
    duck_id = request.args.get('duck_id')
    rating = request.form['rating']
    if request.form['moved'] == 'T':
        moved = False # if yes, it was found where we put it
    elif request.form['moved'] == 'F':
        moved = True # if no, it was found somewhere else

    form_data = Response(response_id=response_id, duck_id=duck_id, rating=rating, moved=moved)
    db.session.add(form_data)
    db.session.commit()
    return 'Form submitted successfully!'  # (hopefully)

@app.route('/response-list')
def response_list():
    responses = db.session.execute(db.select(Response)).scalars()
    return render_template('response-list.html', responses=responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)