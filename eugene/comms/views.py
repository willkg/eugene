from flask import Blueprint, render_template


blueprint = Blueprint('comms', __name__,
                      template_folder='templates')


@blueprint.route('/')
def index():
    return render_template('comms/index.html')
