from flask import render_template, redirect, url_for, Blueprint, session, g
from omniscientus.auth import login_required
from omniscientus.utils.info import CATEGORIES


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/dashboard')
@login_required
def dashboard(channel_info=None):
    return render_template('user/dashboard.html', channel_info=channel_info, categories=CATEGORIES)


@bp.route('/videos')
@login_required
def videos():
    return render_template('user/videos.html')


@bp.route('/video')
@login_required
def video():
    return render_template('user/video.html')


@bp.route('/comments')
@login_required
def comments():
    return render_template('user/comments.html')


@bp.route('/followers')
@login_required
def followers():
    return render_template('user/followers.html')


@bp.route('/follower')
@login_required
def follower():
    return render_template('user/follower.html')


@bp.route('/notifications')
@login_required
def notifications():
    return render_template('user/notifications.html')


@bp.route('/account')
@login_required
def account():
    return render_template('user/account.html')


@bp.route('/support_and_feedback')
@login_required
def support_and_feedback():
    return render_template('user/support_and_feedback.html')
