from flask import Blueprint

api = Blueprint('api', __name__)

from .rbac import create, read, delete
