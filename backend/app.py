import os
from flask import Flask, request, jsonify
from kafka import KafkaConsumer
import json
from analysis import analyze_metrics

app = Flask(__name__)

KAFKA_BROKER = os.environ.get("KAFKA_BROKER")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "k8s-metrics")

recommendations = []

def consume_metrics():
    global recommendations
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='advisor-group'
    )
    for message in consumer:
        metrics = message.value
        recs = analyze_metrics(metrics)
        recommendations = recs

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    return jsonify(recommendations)

@app.route("/remediate", methods=["POST"])
def remediate():
    data = request.json
    return jsonify({"status": "Remediation triggered", "details": data})

def lambda_handler(event, context):
    from aws_lambda_powertools.experimental.adapter.flask import FlaskLambda
    flask_lambda = FlaskLambda(app)
    return flask_lambda(event, context) 