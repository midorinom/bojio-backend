from project.extensions import db
from flask import Blueprint, request
from project.service.event_service import *
from project.utilities.custom_exception_factory import *
import traceback

main_event = Blueprint("main_event", __name__)

@main_event.route('/event/test', methods=['GET'])
def event_test():
    return {
        "message": "hello"
    }

@main_event.route('/event/all-events', methods=['GET'])
def retrieve_all_events():
    try:
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

@main_event.route('/event/all-available-events', methods=['GET'])
def retrieve_all_available_events():
    try:
        events = get_available_events()
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
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

@main_event.route('/event/all-attending-events', methods=['GET'])
def retrieve_all_attending_events():
    try:
        events = get_all_events_as_attendee()
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
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
    
@main_event.route('/event/all-events-as-host', methods=['GET'])
def retrieve_all_events_as_host():
    try:
        events = get_all_events_as_host()
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
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

@main_event.route('/event/create', methods=['POST'])
def create():
    try:
        new_event = request.get_json()
        created_event_obj = create_event(new_event)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except ValueError as errerMsg:
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
            "data": created_event_obj
        }, 200

@main_event.route('/event/update', methods=['POST'])
def update():
    try:
        event_with_updates = request.get_json()
        updated_event = update_event(event_with_updates)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except (UserIsNotHostException, EventNotFoundException, ValueError) as errerMsg:
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
            "data": updated_event
        }, 200
    
@main_event.route('/event/delete', methods=['POST'])
def delete():
    try:
        event_id = request.get_json()['event_id']
        # Calls service to perform business logic
        delete_event(event_id)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except (EventNotFoundException, UserIsNotHostException) as errerMsg:
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

@main_event.route('/event/join', methods=['POST'])
def join():
    try:
        event_id = request.get_json()['event_id']
        # Calls service to perform business logic
        join_event(event_id)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except (AlreadyAttendingException, EventAtMaxCapacityException, UserIsHostException, EventNotFoundException, EventHasEndedException) as errerMsg:
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
            "message": "Event successfully joined"
        }, 200
    
@main_event.route('/event/quit', methods=['POST'])
def quit():
    try:
        event_id = request.get_json()['event_id']
        # Calls service to perform business logic
        quit_event(event_id)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except (UserIsHostException, EventNotFoundException, AlreadyWithdrawnException) as errerMsg:
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
            "message": "Withdrawn from event successfully"
        }, 200

@main_event.route('/event/send-invitation', methods=['POST'])
def send_invitation():
    try:
        data = request.get_json()
        send_event_invite(data)
    except UserNotLoggedInException as errerMsg:
        return {
            "status": "error",
            "message": str(errerMsg)
        }, 401
    except (UserNotFoundException, EventNotFoundException, InvitorIsAlsoInviteeException, InviteeAlreadyReceivedException, InviteeIsHostException) as errerMsg:
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
            "message": "Invitation sent successfully"
        }, 200

def rollback_db():
    if main_event.debug == True:
        print(traceback.format_exc())
    db.session.rollback()