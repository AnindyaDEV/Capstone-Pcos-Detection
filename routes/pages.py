from flask import Blueprint, render_template,session,send_from_directory
import os
import json


page_routes = Blueprint("pages", __name__)

@page_routes.route("/")
def home():
    return render_template("index.html")

@page_routes.route("/self-diagnosis")
def self_diagnosis_page():
    return render_template("self_diagnosis.html")

@page_routes.route("/ultrasound")
def ultrasound_page():
    return render_template("ultrasound_upload.html")


@page_routes.route("/menstrual_tracker", methods=["GET"])
def menstrual_page():
    return render_template("menstrual_tracker.html", events=None)

@page_routes.route("/fitness")
def fitness_page():
    risk_data = session.get("pcos_result")  # This comes from the prediction route
    return render_template("fitness.html", risk=risk_data)

@page_routes.route("/nutrition")
def nutrition_page():
    risk_data = session.get("pcos_result")
    
    return render_template("nutrition.html", risk=risk_data)

@page_routes.route("/support")
def support_page():
    return render_template("support.html")

# @page_routes.route("/gynaecologists")
# def gynaecologist_page():
#     return render_template("gynaecologists.html")

# @page_routes.route("/pharmacy")
# def pharmacy_page():
#     return render_template("pharmacy.html")  
    
@page_routes.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


