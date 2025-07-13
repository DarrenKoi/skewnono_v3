from flask import Blueprint

equipment_status_bp = Blueprint('equipment_status', __name__, url_prefix='/equipment-status')

from . import routes