from app import app, db
from flask import request
from service.event_service import create_event, update_event, get_all_events, delete_event
from utilities.custom_exception_factory import IdNotFoundException
import traceback

@app.route('/event/all-events', methods=['GET'])
def retrieve_all_events():
    try:
        # Calls service to perform business logic
        events = get_all_events()
    except Exception:
        rollback_db()
        return {
            "status": "error",
            "message": "Error occurred"
        }, 500
    else:
        return {
            "status": "success",
            "data": events
        }, 200

@app.route('/event/create', methods=['POST'])
def create():
    try:
        new_event = request.get_json()
        created_event_obj = create_event(new_event)
        
    except Exception:
        rollback_db()
        return {
            "status": "error",
            "message": "Error occurred"
        }, 500
    else:
        db.session.commit()
        return {
            "status": "success",
            "data": created_event_obj
        }, 200

@app.route('/event/update', methods=['POST'])
def update():
    try:
        event_with_updates = request.get_json()
        update_event(event_with_updates)

    except IdNotFoundException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 400
    except Exception:
        rollback_db()
        return {
            "status": "error",
            "message": "Error occurred"
        }, 500
    else:
        db.session.commit()
        return {
            "status": "success",
            "message": "Event successfully updated"
        }, 200
    
@app.route('/event/delete', methods=['POST'])
def delete():
    try:
        event = request.get_json()
        # Calls service to perform business logic
        delete_event(event)
    except IdNotFoundException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 400
    except Exception:
        rollback_db()
        return {
            "status": "error",
            "message": "Error occurred"
        }, 500
    else:
        db.session.commit()
        return {
            "status": "success",
            "message": "Event successfully deleted"
        }, 200

def rollback_db():
    if app.debug == True:
        print(traceback.format_exc())
    db.session.rollback()