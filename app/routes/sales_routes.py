from flask import Blueprint, request, jsonify
from app.services.sales_service import create_sale

sales_bp = Blueprint("sales", __name__)

@sales_bp.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()

    try:
        result = create_sale(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
