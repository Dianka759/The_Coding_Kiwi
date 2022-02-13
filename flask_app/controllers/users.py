from flask_app import app
from flask import render_template, flash, redirect, request, session, url_for
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_bcrypt import Bcrypt

import urllib.request
import os


bcrypt = Bcrypt(app)


UPLOAD_FOLDER = 'flask_app/static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")

#  ====================================
#  Login and registration stuffs
#  ====================================

@app.route("/register", methods=["POST"])
def register():
    if User.validate(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "role": request.form["role"],
            "email": request.form["email"],
            "password": pw_hash
        }
        user_id = User.insert_user(data)
        session["user_id"] = user_id
        return redirect(f"/edit_user/{user_id}")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("invalid email/password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid email/password", "login")
        return redirect("/")
    session["user_id"] = user_in_db.id   # CREATES THE SESSION
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")

# ==========================================
#  Main page
#  =========================================


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    else:
        data = {
            "user_id": session["user_id"]
        }
        user = User.get_user(data)
        return render_template("dashboard.html", user=user)


# @app.route("/create_student")
# def edit_profile():
#     if "user_id" not in session:    #checks if you're logged in
#         flash("Must be registered or logged in!", "register")
#         return redirect("/")
#     return render_template("create_student_profile.html", user=user)

@app.route("/edit_user/<int:user_id>")
def edit_user(user_id):
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "user_id": user_id
    }
    user = User.get_user(data)
    return render_template('edit_user.html', user=user)


@app.route("/update_pic", methods=["POST"])
def update_pic():
    file = request.files['photo']
    filename = (file.filename)
    data = {
        "photo": filename,
        "user_id": session["user_id"]
    }
    if filename != "":
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        User.insert_photo(data)
        # session["photo"] = photo
    else:
        flash("must give a photo to display first!")
    user = User.get_user(data)
    return render_template('edit_user.html', user=user,  filename=filename)


@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    if "student" in session:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form['last_name'],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "password": pw_hash,
            "birthday": request.form["birthday"],
            "summary": request.form["summary"],
            "instructor": request.form["instructor"],
            "current_stack": request.form["current_stack"],
            # "photo":request.form["photo"],
            "id": id
        }
        User.update_student(data)
    else:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form['last_name'],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "password":  pw_hash,
            "birthday": request.form["birthday"],
            "summary": request.form["summary"],
            # "photo":request.form["photo"],
            # "students":request.form["students"],
            "current_stack": request.form["current_stack"],
            "id": id
        }
        User.update_instructor(data)
    return redirect("/your_cohort")
    # else:
    #     return redirect(f"/edit/{id}")


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route("/lectures")
def lectures():
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "user_id": session["user_id"]
    }
    user = User.get_user(data)
    return render_template("lectures.html", user=user)


@app.route("/notes")
def notes():
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "user_id": session['user_id'],
    }
    user = User.get_user(data)
    notes = Note.get_notes()
    return render_template("new_note.html", notes=notes, user=user)


@app.route("/new_note/<int:user_id>", methods=["POST"])
def new_note(user_id):
    data = {
        "user_id": user_id,
        "title": request.form["title"],
        "content": request.form['content'],
    }
    Note.insert_note(data)
    return redirect("/notes")


@app.route("/show_note/<int:id>")
def show_note(id):
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    user = User.get_user(data)
    note = Note.get_note(data)
    notes = Note.get_notes()
    return render_template("show_note.html", user=user, note=note, notes=notes)


@app.route("/edit_note/<int:id>")
def edit_note(id):
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    user = User.get_user(data)
    note = Note.get_note(data)
    notes = Note.get_notes()
    return render_template("update_note.html", user=user, note=note, notes=notes)


@app.route("/update_note/<int:id>", methods=["POST"])
def update_note(id):
    # if Recipe.validate_recipe(request.form):
    data = {
        "title": request.form["title"],
        "content": request.form['content'],
        "id": id
    }
    Note.update_note(data)
    return redirect(f"/show_note/{id}")
    # else:
    #     return redirect(f"/edit/{id}")


# ==========================================
#  Delete note
#  =========================================

@app.route("/delete/<int:id>")
def delete_note(id):
    data = {
        "id": id
    }
    Note.delete_note(data)
    return redirect("/notes")

# ==========================================
#  Edit note
#  =========================================


@app.route("/your_cohort")
def your_cohort():
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    # filename = session["photo"]
    data = {
        # "photo":filename,
        "user_id": session["user_id"]
    }
    user = User.get_user(data)
    users = User.get_all()
    return render_template("your_cohort.html", user=user, users=users)


@app.route('/your_cohort', methods=['POST'])
def upload_image():
    data = {
        "user_id": session["user_id"]
    }
    user = User.get_user(data)
    users = User.get_all()
    return render_template('your_cohort.html', user=user, users=users)


@app.route("/show_person/<int:user_id>")
def show_person(user_id):
    if "user_id" not in session:  # checks if you're logged in
        flash("Must be registered or logged in!", "register")
        return redirect("/")
    data = {
        "user_id": user_id
    }
    user = User.get_user(data)
    return render_template("show_person.html", user=user)
