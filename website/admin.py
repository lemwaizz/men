# app/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import GarbageCollection
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    garbage_collections = GarbageCollection.query.all()
    return render_template('admin/dashboard.html', garbage_collections=garbage_collections)

@admin.route('/collection/add', methods=['GET', 'POST'])
@login_required
def add_collection():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        garbage_type = request.form['type']

        new_collection = GarbageCollection(date=date, time=time, location=location, garbage_type=garbage_type)
        db.session.add(new_collection)
        db.session.commit()
        flash('Garbage collection added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_collection.html')

@admin.route('/collection/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_collection(id):
    collection = GarbageCollection.query.get_or_404(id)

    if request.method == 'POST':
        collection.date = request.form['date']
        collection.time = request.form['time']
        collection.location = request.form['location']
        collection.garbage_type = request.form['type']

        db.session.commit()
        flash('Garbage collection updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_collection.html', collection=collection)

@admin.route('/collection/delete/<int:id>', methods=['POST', 'DELETE'])
@login_required
def delete_collection(id):
    collection = GarbageCollection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    flash('Garbage collection deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
