import qrcode
import uuid
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    rating = db.Column(db.Float())

@app.route('/')
def generate_qr_code():
    unique_id = str(uuid.uuid4())
    url = f'http://127.0.0.1:5000/form?id={unique_id}'
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr_code_{unique_id}.png")
    return f'<img src="qr_code_{unique_id}.png" alt="QR code">'

@app.route('/form')
def form():
    unique_id = request.args.get('id')
    return f'''
        <form method="POST" action="/submit?id={unique_id}">
            <label>Rating:</label><input type="text" name="rating"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    unique_id = request.args.get('id')
    rating = request.form['rating']
    form_data = FormData(id=unique_id, rating=rating)
    db.session.add(form_data)
    db.session.commit()
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, ssl_context='adhoc')