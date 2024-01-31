from db.models import app
from userdir.routes import router
from booksdir.routes import bookrouter

app.register_blueprint(router)
app.register_blueprint(bookrouter)

if __name__ == "__main__":
    app.run(debug = True)