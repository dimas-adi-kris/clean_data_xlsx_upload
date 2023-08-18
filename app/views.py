from app import app

from app.controllers.AdminController import admin 
from app.controllers.HomeController import home,auth
from app.controllers.ExcelOperationController import excel

app.register_blueprint(admin)
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(excel)


