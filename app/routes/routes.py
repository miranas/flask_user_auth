from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message":"Welcome to your Flask app!"})

@main.route("/index")
def olemajole():
    return jsonify({"Message2" : "Welcome to index!"})





