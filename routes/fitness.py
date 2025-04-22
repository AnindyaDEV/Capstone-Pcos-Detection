from flask import Blueprint, request, jsonify
from utils.fitness_utils import get_routines_for_constraint

fitness_routes = Blueprint("fitness", __name__)

@fitness_routes.route("/get_routines", methods=["GET"])
def get_routines():
    constraint = request.args.get("constraint", "").strip()
    if not constraint:
        return jsonify({"error": "Constraint not provided"}), 400
    
    routines = get_routines_for_constraint(constraint)
    if not routines:
        return jsonify({"message": f"No routines found for '{constraint}'"}), 404
    
    return jsonify({"routines": routines})
