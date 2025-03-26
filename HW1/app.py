from flask import Flask, render_template, request, jsonify
import os
import json
from utils import evaluate_policy

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    grid_size = None
    if request.method == "POST":
        try:
            grid_size = int(request.form["grid_size"])
            if not (5 <= grid_size <= 9):
                grid_size = None
        except ValueError:
            grid_size = None
    return render_template("index.html", grid_size=grid_size)

@app.route("/save_map", methods=["POST"])
def save_map():
    data = request.get_json()
    with open("map_data.json", "w") as f:
        json.dump(data, f)
    return jsonify({"message": "地圖儲存成功！"})

@app.route("/evaluate", methods=["GET"])
def evaluate():
    with open("map_data.json", "r") as f:
        data = json.load(f)

    grid_size = data["size"]
    start = data["start"]
    end = data["end"]
    obstacles = data["obstacles"]

    V, policy = evaluate_policy(grid_size, start, end, obstacles)

    # 將 V 轉為可顯示的 2D list（四捨五入）
    value_matrix = [[round(float(v), 2) for v in row] for row in V]
    policy_matrix = policy.tolist()

    return render_template("evaluate.html",
                           value_matrix=value_matrix,
                           policy_matrix=policy_matrix,
                           size=grid_size)

if __name__ == "__main__":
    app.run(debug=True)
