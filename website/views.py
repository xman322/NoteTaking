from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note
import json
views = Blueprint('views', __name__)

headings = ("name", "role", "salary")
data=(("rolf", "product ownwer", "55k"), ("amy", "eng", "99k"), ("bob", "sec eng", "100k"), ("rolf", "product ownwer", "55k"), ("amy", "eng", "99k"), ("bob", "sec eng", "100k"))

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
           
    return render_template("home.html" , user=current_user, headings = headings, data = data)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

  