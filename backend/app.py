from flask import Flask, jsonify
from flask_cors import CORS

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/api/trip", methods=["GET"])
def get_trip():
    items = [
        { "product": '12 personers glamping lavvo', "quantity": 1, "packed": False },
        { "product": 'Grytesett, 2L + 1L gryter, 2x tallerken', "quantity": 1, "packed": False},
        { "product": 'Zenbivy sovesystem', "quantity": 1, "packed": False},
        { "product": 'Retro Campingvogn', "quantity": 1, "packed": False},
        { "product": 'Fargerik Hengekøye', "quantity": 1, "packed": False},
        { "product": 'Bærbar Grill', "quantity": 1, "packed": False},
        { "product": 'Utendørs Projektor og Lerret', "quantity": 1, "packed": False},
        { "product": 'Stjernetittende Teleskop', "quantity": 1, "packed": False},
        { "product": 'Sammenleggbar Campingstol', "quantity": 1, "packed": False},
        { "product": 'Varmt Kakaosett', "quantity": 1, "packed": False},
        { "product": 'Vandrestaver', "quantity": 1, "packed": False},
        { "product": 'Vanntett Kart og Kompass', "quantity": 1, "packed": False},
        { "product": 'Fotovennlig Kamera', "quantity": 1, "packed": False }
    ]
    return jsonify(items)

if __name__ == "__main__":
    app.run()
