from flask import Blueprint, jsonify, request

from app.services.ontology_operations import get_all_skills, skill_hierarchy
from app.services.sanchez_calculator import calculate_sanchez_similarity

similarity_bp = Blueprint("similarity", __name__)


@similarity_bp.route("/skills", methods=["GET"])
def get_skills():
    skills = get_all_skills()
    return jsonify({"skills": skills})


@similarity_bp.route("/calculate_similarity", methods=["POST"])
def calculate_similarity():
    data = request.get_json()
    skills_list_1 = data.get("skills_list_1", [])
    skills_list_2 = data.get("skills_list_2", [])

    if not isinstance(skills_list_1, list) or not isinstance(skills_list_2, list):
        return (
            jsonify({"error": "Both skills_list_1 and skills_list_2 should be lists."}),
            400,
        )

    similarity_score = calculate_sanchez_similarity(skills_list_1, skills_list_2)

    return jsonify({"similarity_score": similarity_score})


@similarity_bp.route("/skill_hierarchy/<skill_name>", methods=["GET"])
def get_skill_hierarchy(skill_name):
    hierarchy = skill_hierarchy(skill_name)
    return jsonify({"skill": skill_name, "hierarchy": hierarchy})
