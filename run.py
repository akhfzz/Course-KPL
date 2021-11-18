from app.views import app 
from app.models import db

if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()