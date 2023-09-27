from app import app, db
from flask import jsonify, request
from service.demo_service import get_message, add_message, update_message, delete_message
from utilities.custom_exception_factory import MessageExistsException, IdNotFoundException
import traceback

@app.route('/demo/get', methods=['GET'])
def demo_get():
    try:
        # Calls service to perform business logic
        result = get_message()
    except Exception:
        rollback_db()
        return {
            "status": "failed",
            "message": "Error occurred"
        }, 500
    else:
        return jsonify(result)

# @app.route('/demo/add', methods=['POST'])
# def demo_add():
#     try:
#         data = request.get_json()
#         # Calls service to perform business logic
#         added_msg_obj = add_message(data)
#     except MessageExistsException as e:
#         return {
#             "status": "failed",
#             "message": str(e)
#         }, 409
#     except Exception:
#         rollback_db()
#         return {
#             "status": "failed",
#             "message": "Error occurred"
#         }, 500
#     else:
#         db.session.commit()
#         return jsonify(added_msg_obj)
    
@app.route('/demo/update', methods=['POST'])
def demo_update():
    try:
        data = request.get_json()
        # Calls service to perform business logic
        update_message(data)
    except IdNotFoundException as e:
        return {
            "status": "failed",
            "message": str(e)
        }, 400
    except MessageExistsException as e:
        return {
            "status": "failed",
            "message": str(e)
        }, 409
    except Exception:
        rollback_db()
        return {
            "status": "failed",
            "message": "Error occurred"
        }, 500
    else:
        db.session.commit()
        return {
            "status": "success",
            "message": "Successfully updated"
        }, 200

@app.route('/demo/delete', methods=['POST'])
def demo_delete():
    try:
        data = request.get_json()
        # Calls service to perform business logic
        delete_message(data)
    except IdNotFoundException as e:
        return {
            "status": "failed",
            "message": str(e)
        }, 400
    except Exception:
        rollback_db()
        return {
            "status": "failed",
            "message": "Error"
        }, 500
    else:
        db.session.commit()
        return {
            "status": "success",
            "message": "Successfully deleted"
        }, 200

def rollback_db():
    if app.debug == True:
        print(traceback.format_exc())
    db.session.rollback()