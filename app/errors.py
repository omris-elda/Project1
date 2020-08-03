from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404
# this handles 404 page not found errors, 
# making the error page a bit more in line with the rest of the app

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500

# this handles 500 database errors 
# (such as duplicated info that's slipped through any other error checking)
# and makes the error page a bit more in line with the rest of the app