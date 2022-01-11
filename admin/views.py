from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User
from functools import wraps

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

# ROLE ACCESS CONTROL
def required_roles(*roles, source):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # redirect user to 403 error page
                return render_template('error_codes/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper

# view admin page
@admin_blueprint.route('/admin')
@login_required
@required_roles('admin', source='Admin Page')
def admin():
    return render_template('admin.html', lastname=current_user.lastname)


# view all users
@admin_blueprint.route('/view_users', methods=['POST'])
@login_required
@required_roles('admin', source='Admin Page - view users')
def view_users():
    return render_template('admin.html', lastname=current_user.lastname,
                           all_users=User.query.all())


# view security logging data (last 15 log records)
@admin_blueprint.route('/logging', methods=['POST'])
@login_required
@required_roles('admin', source='Admin Page - security log')
def logging():
    # read last 15 log records
    with open("user_logs.log", "r") as f:
        content = f.read().splitlines()[-15:]
        content.reverse()

    return render_template('admin.html', lastname=current_user.lastname, logs=content)


# view whole security log
@admin_blueprint.route('/seclog', methods=['POST'])
@login_required
@required_roles('admin', source='Admin Page - full security log')
def full_logging():
    # read whole log
    with open("user_logs.log", "r") as f:
        content = f.read().splitlines()
        content.reverse()

    return render_template('security_log.html', logs=content)
