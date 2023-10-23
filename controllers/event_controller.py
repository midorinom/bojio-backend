from app import app, db
from flask import jsonify, request
from service.event_service import create_event
import traceback

@app.route('/event/create', methods=['POST'])
def create():
    try:
        data = request.get_json()
        created_event_obj = create_event(data)
    except Exception:
        rollback_db()
        return {
            "status": "error",
            "message": "Error occurred"
        }, 500
    else:
        db.session.commit()
        return jsonify(created_event_obj)

def rollback_db():
    if app.debug == True:
        print(traceback.format_exc())
    db.session.rollback()