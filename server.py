from flask import Flask, request, jsonify
from flask_cors import CORS
from db_model import User, Schedule, Client_Device, session, generate_random_code
from passlib.hash import sha256_crypt
from datetime import datetime, time
from generals import ExtractTime

app = Flask(__name__)
CORS(app)
app.config["session_tokens"] = []

session_token = {
    "user_id": "",
    "token": "",
    "created_at": ""
}

@app.route("/")
def Home():
    return "Home"

@app.route("/user/<string:args>", methods=["POST", "GET"])
def UserAccess(args=None):
    method = request.method
    if method == 'GET':
        pass

    if method == 'POST':
        if args == "create":
            request_data = request.get_json()
            name = request_data["name"]
            email = request_data["email"]
            phone = request_data["phone"]
            password = sha256_crypt.hash(request_data["password"])
            try:
                user = User(name=name, email=email, phone=phone, password=password)
                session.add(user)
                session.commit()
                req_state = True
                req_message = "Account created Successfully"
            except:
                session.rollback()
                req_state = False
                req_message = "Could not create user account"
        
        if args == "update":
            pass

    return jsonify(
        {
            "state": req_state,
            "message": req_message
        }
    ), 200

@app.route("/auth", methods=["POST"])
def Authentication():
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    user = session.query(User).filter_by(email=email).first()
    
    if user and sha256_crypt.verify(password, user.password):
        access_token = generate_random_code()
        session_token = {
            "user_id": user.id,
            "token": access_token,
            "created_at": datetime.now()
        }
        app.config["session_tokens"].append(session_token)
        response = {
            "state": True,
            "message": "Authenticated Successfully",
            "access_token": access_token
        }
        return jsonify(response)
    else:
        response = {
            "state": False,
            "message": "User Authentication Failed",
            "access_token": None
        }
        return jsonify(response)
    
@app.route("/device/<string:args>", methods=["POST"])
@app.route("/device", methods=["GET"])
def Devices(args=None):
    method = request.method

    if method == 'GET':
        devices = session.query(Client_Device).all()
        devices = [
            {"id":device.id, 
             "name": device.name, 
             "state": device.state,
             "updated_at": device.updated_at,
             "created_time": device.created_at
             }
             for device in devices
             ]
        return jsonify(devices), 200
    
    if method == 'POST':
        device_id = request.get_json()["device_id"]
        device = session.query(Client_Device).filter_by(id=device_id).first()

        if args == "update":
            device_name = request.get_json()["device_name"]
            device.name = device_name
        if args == "toggle":
            device.state = not device.state
        if args == "delete":
            session.delete(device)
        session.commit()
        return jsonify(
            {
                "state": True
            }
        ), 200

@app.route("/schedule/<string:device_id>/<string:schedule_id>/<string:args>", methods=["POST"])
@app.route("/schedule/<string:device_id>/<string:schedule_id>", methods=["GET"])
def Schedules(args=None, device_id=None, schedule_id=None):
    method = request.method
    
    device = session.query(Client_Device).filter_by(id=device_id).first()
    schedule = session.query(Schedule).filter_by(id=schedule_id).first()
    
    if method == "GET":
        device_schedules = device.schedules
        print(device_schedules)
        schedules = [
            {"id": schedule.id,
             "device_id": schedule.device_id,
             "name": schedule.name,
             "execute_at": schedule.execute_at.strftime("%H:%M"),
             "duration": schedule.duration,
             "state": schedule.state,
             }
             for schedule in device_schedules
             ]
        print(schedules)
        return jsonify(schedules)
    
    if method == "POST":
        if args == "create":
            name = request.get_json()["name"]
            executed_at = ExtractTime(request.get_json()["executed_at"])
            duration = request.get_json()["duration"]
            print(name)
            print(executed_at)
            print(type(executed_at))
            print(request.get_json()["executed_at"])
            print(duration)
            schedule = Schedule(name=name, execute_at=time(executed_at[0], executed_at[1]), duration=duration, device=device)
            session.add(schedule)
            session.commit()
            new_schedule = {
                "device_id": device_id,
                "duration": duration,
                "execute_at": f"{executed_at[0]}:{executed_at[1]}",
                "id": schedule.id,
                "name": name,
                "state": True
            }
            

            return jsonify(new_schedule)

        if args == "update":
            name = request.get_json()["name"]
            executed_at = ExtractTime(request.get_json()["executed_at"])
            print(f"{'-'*20} {executed_at} {'-'*20}")
            print(request.get_json()["executed_at"])
            duration = request.get_json()["duration"]
            schedule.name = name
            schedule.execute_at = time(executed_at[0], executed_at[1])
            schedule.duration = duration
            session.commit()

        if args == "toggle":
            schedule.state = not schedule.state

        if args == "delete":
            session.delete(schedule)

        session.commit()
    
        return jsonify(["cioewijce"])


if __name__ == "__main__":
    app.run(debug=True, port=8080)
    # app.run(debug=True, port=443)