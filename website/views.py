# views.py

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import GarbageCollection
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        garbage_type = request.form.get('type')

        if not (date and time and location and garbage_type):
            flash('Please fill out all fields.', category='error')
        else:
            new_collection = GarbageCollection(date=date, time=time, location=location, garbage_type=garbage_type, user_id=current_user.id)
            db.session.add(new_collection)
            db.session.commit()
            flash('Garbage collection added successfully!', category='success')

    garbage_collections = GarbageCollection.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, garbage_collections=garbage_collections)

@views.route('/delete-collection', methods=['POST'])
@login_required
def delete_collection():
    collection = json.loads(request.data)
    collection_id = collection['collectionId']
    collection = GarbageCollection.query.get(collection_id)
    
    if collection:
        if collection.user_id == current_user.id:
            db.session.delete(collection)
            db.session.commit()
            flash('Garbage collection deleted successfully!', category='success')
    
    return jsonify({})
@views.route('/about-us')
def about_us():
    return render_template('about_us.html')
