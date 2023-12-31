from flask import Flask
from flask_cors import CORS,cross_origin
import paho.mqtt.client as mqtt
import json
from include.config import BROKER, CERT, PORT

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*", "methods": "*", "headers": "*"}})

@cross_origin()
@app.route('/dispenser/stock/<machine_id>/<int:stock>',methods=['POST'])
def dispense_stock(machine_id,stock):
     payload_dict = {
          "stock-updated": stock,
          "machine_id": machine_id
                    }
     json_payload = json.dumps(payload_dict)
     client = mqtt.Client("P1")
     client.tls_set(ca_certs = CERT)
     client.connect(BROKER, PORT)
     client.publish("dispenser/{}/stock".format(machine_id,stock),json_payload)
     print("Update stock to '{}' sent for machine ID: {}".format(stock, machine_id))
     client.disconnect()
     return " "

@cross_origin()
@app.route('/dispenser/dispense/<machine_id>',methods=['POST'])
def dispense(machine_id):
     client = mqtt.Client("P1")
     client.tls_set(ca_certs = CERT)
     client.connect(BROKER, PORT)
     payload_dict = {
          "button-pressed": True,
          "machine_id": machine_id
                    }
     json_payload = json.dumps(payload_dict)

     client.publish("dispenser/{}/dispense_event_ui".format(machine_id), json_payload)
     print("Dispense event sent for machine ID: {}".format(machine_id))
     client.disconnect()  
     return " "

if __name__ == '__main__':
    app.run(debug=True)
