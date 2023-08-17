from app import app

from app.controllers.HomeController import home
from app.controllers.ExcelOperationController import excel

app.register_blueprint(home)
app.register_blueprint(excel)


