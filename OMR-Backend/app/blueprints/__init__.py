from app import app
from app.crud_view.urls import OMR_readblueprint,Answerkey_readblueprint

app.register_blueprint(OMR_readblueprint)

app.register_blueprint(Answerkey_readblueprint)


