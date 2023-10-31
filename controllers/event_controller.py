from app import app, db
from flask import request
from service.event_service import *
from utilities.custom_exception_factory import *
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
        }, 404
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
        data = request.get_json()
        # Calls service to perform business logic
        delete_event(data)
    except IdNotFoundException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 404
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

@app.route('/event/join', methods=['POST'])
def join():
    try:
        data = request.get_json()
        # Calls service to perform business logic
        join_event(data)
    except (UserNotFoundException, EventNotFoundException) as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 404
    except AlreadyAttendingException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 409
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
            "message": "Event successfully joined"
        }, 200
    
@app.route('/event/quit', methods=['POST'])
def quit():
    try:
        data = request.get_json()
        # Calls service to perform business logic
        quit_event(data)
    except (UserNotFoundException, EventNotFoundException) as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 404
    except AlreadyWithdrawnException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 409
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
            "message": "Withdrawn from event successfully"
        }, 200

def rollback_db():
    if app.debug == True:
        print(traceback.format_exc())
    db.session.rollback()