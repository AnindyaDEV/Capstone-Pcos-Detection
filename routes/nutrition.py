from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from utils.nutrition_utils import get_nutrition_info, calculate_macros, generate_meal_plan_with_groq
import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas



nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route("/nutrition")
def nutrition_page():
    return render_template("nutrition.html")

@nutrition_bp.route("/get_nutrition", methods=["POST"])
def get_nutrition():
    data = request.get_json()
    food = data.get("food")

    try:
        result = get_nutrition_info(food)
        items = result['foods']
        info = [{
            "name": item["food_name"],
            "calories": item["nf_calories"],
            "protein": item["nf_protein"],
            "carbs": item["nf_total_carbohydrate"],
            "fat": item["nf_total_fat"]
        } for item in items]
        return jsonify(info[0])
    except Exception as e:
        return jsonify({"error": str(e)})

@nutrition_bp.route("/calculate_macros", methods=["POST"])
def macros():
    data = request.get_json()
    macros = calculate_macros(
        weight=float(data['weight']),
        height=float(data['height']),
        age=int(data['age']),
        gender=data['gender'],
        activity_level=data['activity'],
        goal=data['goal']
    )
    return jsonify(macros)
@nutrition_bp.route("/meal_plan", methods=["POST"])
def meal_plan():
    data = request.get_json()

    try:
        calories = data.get("calories", 1800)
        protein = data.get("protein", 100)
        carbs = data.get("carbs", 200)
        fat = data.get("fat", 50)

        # Generate meal plan using HuggingFace LLM with macros
        meal_plan = generate_meal_plan_with_groq(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat
        )

        return jsonify(meal_plan)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@nutrition_bp.route("/save_meal_plan", methods=["POST"])
def save_meal_plan():
    data = request.get_json()
    meal_plan = data.get("meal_plan")

    if not meal_plan:
        return jsonify({"error": "Meal plan is missing"}), 400

    try:
        pdf_folder = os.path.join(current_app.root_path, "static", "pdf")
        os.makedirs(pdf_folder, exist_ok=True)

        filename = f"meal_plan_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(pdf_folder, filename)

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 40

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"PCOS Diet Plan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 30

        for day, meals in meal_plan.items():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, day.upper())
            y -= 20

            c.setFont("Helvetica", 11)
            for meal_type, details in meals.items():
                title = details.get('title', 'Unnamed Meal')
                calories = details.get('calories', 'N/A')
                protein = details.get('protein', 'N/A')
                carbs = details.get('carbs', 'N/A')
                fat = details.get('fat', 'N/A')

                meal_line = f"{meal_type.title()} (~{calories} kcal): {title} | {protein}g P, {carbs}g C, {fat}g F"
                c.drawString(60, y, meal_line)
                y -= 20
                if y < 60:
                    c.showPage()
                    y = height - 40

            y -= 10

        c.save()

        return jsonify({
            "message": "Meal plan saved as PDF!",
            "pdf_url": f"/static/pdf/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

