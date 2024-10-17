from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('login'))
    return render_template('register.html', form = form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username = form.username.data).first()
            
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('account'))
            else:
                flash("Login failed!")
    return render_template('login.html', form = form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            current_user.modify(username=update_username_form.username.data)
            current_user.save()

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            profile_pic_form = update_profile_pic_form.picture.data.read()
            profile_pic_form_base64 = base64.b64encode(profile_pic_form.getvalue()).decode()
            
            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(profile_pic_form_base64)
            else:
                current_user.replace(profile_pic=profile_pic_form_base64)
            current_user.save()
        return render_template("account.html", image = current_user.profile_pic)