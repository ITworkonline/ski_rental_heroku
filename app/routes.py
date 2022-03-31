from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, ManagerForm, SkiForm
from app.models import User, Ski

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)  # hash to project password
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registration success! Book the bike now!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
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

#logout methods
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#base customer page
@app.route('/customer')
@login_required
def customer():
    return render_template('customer.html')

#base manager page
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

#manager sub page
@app.route('/admin',methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


#manager dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    ski = Ski.query.all()
    return render_template('dashboard.html', skis=ski)


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


@app.route('/delete_ski/<string:id>', methods=['POST'])
@login_required
def delete_ski(id):
    deleted = Ski.query.filter_by(id=id).first()
    db.session.delete(deleted)
    db.session.commit()
    flash('Ski Deleted', 'success')
    return redirect(url_for('dashboard'))
