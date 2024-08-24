from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('lobby', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')
