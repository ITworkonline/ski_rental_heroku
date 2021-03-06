from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, ManagerForm, SkiForm, EditForm, PasswordResetRequestForm, \
    ResetPasswordForm
from app.models import User, Ski
from app.email import send_reset_password_mail

"""
Global var:
API_DATA: Pass the request data through diff func
FLAG: Only pop up one data when POST 
"""
API_DATA = 1
FLAG = True


# root route
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# API receiver
@app.route('/key', methods=['GET', 'POST'])
def weather_req():
    global FLAG
    global API_DATA
    if FLAG:
        FLAG = False
        API_DATA = request.data
        return API_DATA
    return API_DATA


# about route
@app.route('/about', methods=['GET', 'POST'])
def about():
    context = weather_req().decode("utf-8")
    return render_template('about.html', temp=context)


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    # store the username, email, and password in db
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)  # hash to project password
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registration success! Book the ski now!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        # check with the database
        if user and bcrypt.check_password_hash(user.password, password):
            # user exist and password matched
            login_user(user, remember=remember)

            flash('Login success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('User not exists or password not match', category='danger')
    return render_template('login.html', form=form)


# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# base customer route
@app.route('/customer')
@login_required
def customer():
    return render_template('customer.html')


# base manager route
@app.route('/manager', methods=['GET', 'POST'])
@login_required
def manager():
    form = ManagerForm()
    password = form.password.data
    # super user password
    if password != '12345':
        flash('password not match', category='danger')
    else:
        return redirect(url_for('admin'))
    return render_template('manager.html', form=form)


# manager sub route
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


# manager dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    ski = Ski.query.all()
    return render_template('dashboard.html', skis=ski)


# add route
@app.route('/add_ski', methods=['GET', 'POST'])
@login_required
def add_ski():
    form = SkiForm(request.form)
    if request.method == 'POST' and form.validate():
        ski_brand = form.ski_brand.data
        ski_type = form.ski_type.data
        price = form.price.data
        availability = 'Yes'
        insert(ski_brand, ski_type, price, availability)

        flash('Ski added', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_ski.html', form=form)


def insert(ski_brand, ski_type, price, availability):
    ski = Ski(ski_brand=ski_brand, ski_type=ski_type, price=price, availability=availability)
    db.session.add(ski)
    db.session.commit()


# delete route
@app.route('/delete_ski/<string:id>', methods=['POST'])
@login_required
def delete_ski(id):
    deleted = Ski.query.filter_by(id=id).first()
    db.session.delete(deleted)
    db.session.commit()
    flash('Ski Deleted', 'success')
    return redirect(url_for('dashboard'))


# edit route
@app.route('/edit_ski/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_ski(id):
    edited = Ski.query.filter_by(id=id).first()
    form = EditForm(request.form)
    # get the data from db
    form.ski_brand.data = edited.ski_brand
    form.ski_type.data = edited.ski_type
    form.price.data = edited.price
    form.availability.data = edited.availability

    if request.method == 'POST' and form.validate():
        ski_brand = request.form['ski_brand']
        ski_type = request.form['ski_type']
        price = request.form['price']
        availability = request.form['availability']
        edited.ski_brand = ski_brand
        edited.ski_type = ski_type
        edited.price = price
        edited.availability = availability
        detail_date = datetime.now()

        edited.modification_time = detail_date
        db.session.commit()

        flash('Ski equipment Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_ski.html', form=form)


# choose route
@app.route('/customer/<string:ski_brand>', methods=['GET', 'POST'])
@login_required
def choose_ski(ski_brand):
    choice = Ski.query.filter_by(ski_brand=ski_brand)
    filtered_choice = []
    # check the db if certain brand is available or not
    if choice.first() is None:
        flash('No {} available right now, please choose other brands or contact with the manager'.format(ski_brand),
              category='danger')
        print('no brand case')
        return redirect(url_for('customer'))

    for i in range(len(choice.all())):
        if choice.all()[i].availability == 'Yes':
            filtered_choice.append(choice.all()[i])
    if not filtered_choice:
        flash('No {} available right now, please choose other brands or contact with the manager'.format(
            ski_brand), category='danger')
        print('all booked case')
        return redirect(url_for('customer'))

    return render_template('choose_ski.html', skis=filtered_choice)


# booking route
@app.route('/customer/pay/<string:id>', methods=['GET', 'POST'])
@login_required
def book_ski(id):
    booked = Ski.query.filter_by(id=id)
    return render_template('book_ski.html', skis=booked)


# successful booking route
@app.route('/successful/<string:id>', methods=['GET', 'POST'])
@login_required
def successful(id):
    availability = 'Booked by ' + current_user.username
    book_time = datetime.now()
    # after booking, update the certain ski be 'No' availability
    ski = Ski.query.filter_by(id=id)
    ski.first().availability = availability
    ski.first().modification_time = book_time
    db.session.commit()
    return render_template('successful.html', skis=ski)


# statistic route
@app.route('/statistic', methods=['GET', 'POST'])
@login_required
def statistic():
    return render_template('statistic.html')


# statistic sub route
@app.route('/statistic/<string:ski_brand>', methods=['GET', 'POST'])
@login_required
def statistic_car(ski_brand):
    brand_overview = Ski.query.filter_by(ski_brand=ski_brand)
    count = 0
    filtered_brand_overview = []
    # count the price summary for the certain brand
    for i in range(len(brand_overview.all())):
        if brand_overview.all()[i].availability != 'Yes':
            count += brand_overview.all()[i].price
            filtered_brand_overview.append(brand_overview.all()[i])
    return render_template('statistic_ski.html', skis=filtered_brand_overview, counts=count)


# send password route
@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    # if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    # get the email, user from db, send the mail
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('Password reset request mail is set! Please check your mail.', category='info')
    return render_template('send_password_reset_request.html', form=form)


# reset password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    # validate the token, change the password
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password reset is Done! You can login now', category='info')
            return redirect(url_for('login'))
        else:
            flash('The user is not exist', category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
