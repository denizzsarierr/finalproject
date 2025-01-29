from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import current_user,login_required
from .models import Note
from . import models,db
import json
views = Blueprint("views",__name__)


@views.route('/',methods = ["GET","POST"])
@login_required
def home():

    form = request.form

    if request.method == "POST":
        note = form.get("note")
        
        if len(note) > 0:
            new_note = models.Note(data = note,user_id = current_user.id)

            db.session.add(new_note)
            db.session.commit()

            flash("Note Added",category="success")
            return redirect(url_for('views.home'))
    return render_template("home.html",user = current_user)


@views.route("/delete-note",methods = ["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    if note:

        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})




