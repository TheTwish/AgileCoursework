from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.events.forms import AddEventForm, EditEventForm, ReviewForm, CategoryForm, EditCategoryForm
from app.models import Event, Review
#from app.funcs import save_picture
from app import db
from sqlalchemy.sql import func, or_
from flask_login import current_user, login_user, logout_user, login_required

events = Blueprint('events', __name__)

@events.route('/all_events')
def all_events():
    return 'All events page'

@events.route('/new_event', methods=['GET', 'POST'])
@login_required
def new_event():
    form = AddEventForm()
    #form.category_id.choices = [(c.id, c.name.title()) for c in Category.query.all()]
    if form.validate_on_submit():
        image_file = 'default.jpg'
        if form.image.data:
            image_file = save_picture(form.image.data)
  
        event = Event(
            name=form.name.data,
            host=form.host.data,
            summary=form.summary.data,
            image=image_file,
            location=form.location.data,
            date = form.date.data,
            price=form.price.data,
            #category_id=form.category_id.data
        )
        db.session.add(event)
        db.session.flush()
        new_id = event.id
        db.session.commit()
        flash('Event was added successfully', 'success')
        return redirect(url_for('events.event', id=new_id))
    return render_template('events/new_event.html', title='Add event', form=form)

@events.route('/event/<id>', methods=['GET', 'POST'])
def event(id):
    event = Event.query.get(id)#Get event with respective ID
    form = ReviewForm()
    temp = db.session.query(func.avg(Review.rating).label('average')).filter(Review.event_id == id)
    if temp[0].average:#If it has one or more reviews, find the average
        avg = round(temp[0].average, 2) 
    else: #If no reviews are posted set it to 0 stars
        avg = 0

    if form.validate_on_submit():#If user submits a form, check validity
        rev = Review.query.filter_by(event_id=id, user_id=current_user.get_id()).count()#set rev to previous review of event
        #will be 0 if no previous review is posted
        if rev != 0:#if rev is not equal to 0 a reviews has already been posted. Promt user to edit current review
            flash("Can't review an event twice. Please edit/update your previous review", "warning")
        else:#otherwise create new instance of Review, assigning it data from the form
            review = Review(
                rating = round(form.rating.data, 2),
                text = form.text.data,
                user_id = current_user.get_id(),
                event_id = id
            )
            flash("Review has been added", "success")
            db.session.add(review)#add the review to the current session and commit it
            db.session.commit()
        return redirect(url_for('events.event', id=id))#redirect user back to the event's page
    return render_template('events/event.html', name=event.name.title(), event=event, form=form, average=avg)

@events.route('/search', methods=['GET', 'POST'])
def search():
    events = None
    target_string = request.form['search']

    events = Event.query.filter(
        or_(
            Event.name.contains(target_string),
            Event.host.contains(target_string)
            )
        ).all()

    if target_string == '':
        search_msg = 'No record(s) found - displaying all records'
        color = 'danger'
    else:
        search_msg = f'{len(events)} event(s) found'
        color = 'success'
    return render_template('events/search.html', 
        title='Search result', events=events, 
        search_msg=search_msg, color=color
    )

@events.route('/event/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    if Event.query.filter_by(id=id).delete():
        db.session.commit()
        flash ('Event has been deleted', 'success')
        return redirect(url_for('main.index'))
    return redirect(url_for('events.event', id=id))

@events.route('/event/<id>/edit_review', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    review = Review.query.filter_by(event_id=id, user_id=current_user.get_id())[0]
    form = ReviewForm()
    if request.method == 'GET':
        form.text.data = review.text 
    if form.validate_on_submit() and request.method == 'POST':
        review.rating = round(form.rating.data, 2)
        review.text = form.text.data
        db.session.commit()
        return redirect(url_for('events.event', id=id))
    return render_template('events/edit_review.html', title="Edit review", form=form, id=id)

@events.route('/event/<id1>/delete_review/<id2>', methods=['GET', 'POST'])
@login_required
def delete_review(id1, id2):
    if Review.query.filter_by(id=id2).delete():
        db.session.commit()
        flash ('Review has been deleted', 'success')
        return redirect(url_for('events.event', id=id1))
    return redirect(url_for('events.event', id=id1))  