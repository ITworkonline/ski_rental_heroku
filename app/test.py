import os
import tempfile

import pytest

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, ManagerForm, SkiForm
from app.models import User, Ski


@pytest.fixture
def test_db():
    # Add a user into the db
    username = "test_user_name"
    email = "fake@gmail.com"
    password = bcrypt.generate_password_hash("12345")  # hash to project password
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    # Check if the "test_user_name" exists in the current db
    matches = db.filter(MyUser.title == username)
    self.assert_equal(matches, username)