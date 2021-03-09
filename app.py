from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime
from util import *

from ecom import retrieve_product_name


"""------------------------------------Initializing App and Database------------------------------------"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '256808a4404917c4e708d093936b2ccb'
db = SQLAlchemy(app)
db.create_all()





"""------------------------------------------------Models-----------------------------------------------"""
# from app import db
# db.create_all()

class Footprint(db.Model):
    '''
    Model to store footprint each day
    '''
    id = db.Column(db.Integer, primary_key=True)
    energy = db.Column(db.Float)        # daily footprint from energy in kg
    food = db.Column(db.Float)          # daily footprint from food in kg
    transport = db.Column(db.Float)     # daily footprint from transport in kg
    daily = db.Column(db.Float)         # total daily footprint in kg
    yearly = db.Column(db.Float)        # total yearly footprint in tonnes
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    form = db.Column(db.PickleType())   # form data for recommending
    
    def __repr__(self):
        return '<Footprint %r>' % self.id





"""------------------------------------------------Forms-----------------------------------------------"""
class QuizForm(FlaskForm):
    '''
    Form to obtain necessary data for calculating footprint
    '''
    # Energy
    nRoom = IntegerField("How many rooms do you have?", validators=[InputRequired()])
    nAC = IntegerField("How many hours do you keep the AC on in a day?", validators=[InputRequired()])
    nPC = IntegerField("How many hours do you keep your PC on in a day?", validators=[InputRequired()])
    nLarge = IntegerField("How many large electronic furnitures do you own? (E.g., Refrigerator, Dish Washer)", validators=[InputRequired()])
    # Food
    pMeat = SelectField("What percent of your meal is meat?", choices=[
        (0.1, '0~20%'), (0.3, '20~40%'), (0.5, '40~60%'), (0.7, '60~80%'), (0.9, '80~100%')
    ])
    foodCost = SelectField("How much money do you spend on your food every day?", choices=[
        (200, '<250 yen'), (400, '250~500 yen'), (750, '500~1000 yen'), (1250, '1000~1500 yen'), (1800, '>1500 yen')
    ])
    # Transport
    carSize = SelectField("How big is your car?", choices=[
        (0.00, 'I don\'t own a car'), (0.17, 'small'), (0.22, 'medium'), (0.27, 'large')
    ])
    nCar = IntegerField("How many hours do you ride the car each week?", validators=[InputRequired()])
    nPublic = IntegerField("How many hours do you ride the train or the bus each week?", validators=[InputRequired()])
    nPlane = IntegerField("How many plane rides do you take each year?", validators=[InputRequired()])





"""----------------------------------------Webpage and Rendering----------------------------------------"""
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        pass
    else:
        return render_template('home.html')



@app.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    form = QuizForm()
    if form.validate_on_submit():
        # If form is valid, calculate the footprint and save it into the model
        result = extractForm(form)
        footprint = calcCF(result)
        daily = sum(footprint.values())
        yearly = daily * 0.365
        cf = Footprint(energy=footprint["Energy"], food=footprint["Food"], transport=footprint["Transport"], daily=daily, yearly=yearly, form=result)
        db.session.add(cf)
        db.session.commit()
        return redirect(url_for('quiz_page'))
    
    cf = Footprint.query.order_by(Footprint.date_added.desc()).all()
    return render_template('quiz.html', form=form, cf=cf)


@app.route('/products', methods=['GET'])
def products():
    product_data = retrieve_product_name()
    return render_template('products.html', product_data=product_data)



if __name__ == '__main__':
    app.run()