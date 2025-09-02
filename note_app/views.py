# views.py (updated)
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from datetime import datetime
from note_app import db
from note_app.models import Note
from note_app.forms import NoteForm
from flask_login import current_user, login_required

views2 = Blueprint('views', __name__,template_folder='public')

@views2.route('/', methods=['GET', 'POST'])
@views2.route('/home', methods=['GET', 'POST'])
def home():
    form = NoteForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            note = Note(title=form.title.data, content=form.content.data, user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Your note has been saved!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('You need to be logged in to save notes.', 'warning')
            return redirect(url_for('auth.login'))
    
    notes = []
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_created.desc()).all()
    
    date = datetime.now()
    current_date = date.strftime("%Y")
    return render_template("home.html", title="Home", form=form, notes=notes, current_date=current_date)

@views2.route('/note/<int:note_id>/delete')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('views.home'))


@views2.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    
    date = datetime.now()
    current_date = date.strftime("%Y")
    return render_template("view_note.html", title=note.title, note=note, current_date=current_date)

@views2.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('views.view_note', note_id=note.id))
    
    # Pre-populate the form with existing data
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    
    date = datetime.now()
    current_date = date.strftime("%Y")
    return render_template("edit_note.html", title="Edit Note", form=form, note=note, current_date=current_date)
