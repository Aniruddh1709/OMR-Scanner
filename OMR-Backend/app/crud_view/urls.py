from flask import Blueprint
from flask_restplus import Api
from .resources import OMRREADERView,AnswerKeyReaderView

OMR_readblueprint = Blueprint('OMR_read', __name__, url_prefix='/omrread')
Answerkey_readblueprint = Blueprint('Answer_read', __name__, url_prefix='/answer_read')

api = Api(OMR_readblueprint)
api2 = Api(Answerkey_readblueprint)
api.add_resource(OMRREADERView, '/')
api2.add_resource(AnswerKeyReaderView, '/')


