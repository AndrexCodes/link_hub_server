from flask import Flask, request
from cpanel_db_model import session, Link_Hubs

app = Flask(__name__)
app.config["auth_key"] = "ef8y72cho837hc43874cowuhxo87hecx298302983e94232dhowiucxw"


@app.route("/validateHub", methods=["POST"])
def validateHub():
    public_ip = request.remote_addr
    Authorization = request.headers.get('Authorization')
    linkHub = session.query(Link_Hubs).filter_by(id="email").first()
    if not linkHub:
        new_link_hub = Link_Hubs()

if __name__ == '__main__':
    app.run()