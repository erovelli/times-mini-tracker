from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Entry, User, Group
from . import db
import json
from sqlalchemy.sql import func, desc

""" manage site pages """
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ homepage """

    if request.method == 'POST':
        entry = request.form.get('entry')
        date = request.form.get('date')

        if len(entry) < 1:
            flash('Enter your time!', category='error')
        elif not date:
            flash('Enter date of mini', category='error')
        else:
            test_in = False
            for item in current_user.entries:  # prevent repeat entrys
                if date == item.mini_date:
                    test_in = True
            if not test_in:
                try:
                    entry = float(entry)
                    new_entry = Entry(data=entry, mini_date=date,
                                      user_id=current_user.id)
                    db.session.add(new_entry)
                    db.session.commit()
                    stat_update(user=current_user)

                    flash('Time added!', category='success')
                except:
                    flash('Enter a real number!', category='error')
            else:
                flash('This mini has already been recorded.', category='error')

    return render_template("home.html", user=current_user)


@views.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    """ group page """

    group = Group.query.filter_by(id=current_user.group_id).first()

    for user in group.users:
        print(user.username, user.min, user.id)

    return render_template("group.html", user=current_user, group=group)


@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    """ delete entry """

    entry = json.loads(request.data)
    entryId = entry['entryId']
    entry = Entry.query.get(entryId)
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()

    stat_update(user=current_user)
    return jsonify({})


def stat_update(user):
    if len(current_user.entries) > 0:
        sum = 0
        min = max = current_user.entries[0].data
        for entry in current_user.entries:
            sum += entry.data
            if entry.data < min:
                min = entry.data
            if entry.data > max:
                max = entry.data
        avg = round(sum/len(current_user.entries), 2)

        db.session.query(User).filter_by(id=user.id).update(
            {User.avg_time: avg}, synchronize_session=False)
        db.session.query(User).filter_by(id=user.id).update(
            {User.min: min}, synchronize_session=False)
        db.session.query(User).filter_by(id=user.id).update(
            {User.max: max}, synchronize_session=False)

        db.session.commit()
