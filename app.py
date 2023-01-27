from help.test import load_csv,save_csv,CSV_FILE
from flask import Flask,request ,jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


diamonds = load_csv()
save_csv(diamonds)

df = pd.read_csv(CSV_FILE)


@app.route("/", methods=['GET'])
def start_site():
    return diamonds

@app.route("/max", methods=['GET'])
def max_price():
    max_price = df['price'].max()
    return {'max_price': int(max_price)}

@app.route("/mean", methods=['GET'])
def mean_price():
    mean_price = df['price'].mean()
    return {'mean_price': int(mean_price)}

@app.route("/ideal", methods=['GET'])
def count_ideal():
    ideal_count = df[df['cut']=='Ideal'].shape[0]
    return {'ideal_count': str(ideal_count)}

@app.route("/premium", methods=['GET'])
def count_premium():
    premium_carats = df[df['cut'] == 'Premium']['carat']
    median_carat = premium_carats.median()
    return {'median_carat': str(median_carat)}

@app.route("/avgcut", methods=['GET'])
def avg_carat():
    cut_carat_avg = df.groupby('cut')['carat'].mean()
    # method to convert the DataFrame "cut_carat_avg" to a JSON string
    return {'cut_carat_avg':str(cut_carat_avg)}

@app.route("/colorpa", methods=['GET'])
def color_price_avg():
    color_price_avg = df.groupby('color')['price'].mean()
    # method to convert the DataFrame "color_price_avg" to a JSON string
    return {'color_price_avg':str(color_price_avg)}


@app.route("/add", methods=['POST'])
def add_diamond():
    data = request.get_json()
    diamonds.append(data)
    save_csv(diamonds)
    return data


@app.route("/upd_diamond", methods=['PUT'])
def update_diamond():
    data = request.get_json()
    found = False
    for i,d in enumerate(diamonds):
        if d["ID"] == data["ID"]:
            diamonds[i]["price"] = data["price"]
            # diamonds[i]["carat"] = data["carat"]
            # diamonds[i]["cut"] = data["cut"]
            # diamonds[i]["color"] = data["color"]
            # diamonds[i]["clarity"] = data["clarity"]
            # diamonds[i]["depth"] = data["depth"]
            # diamonds[i]["table"] = data["table"]
            # diamonds[i]["x"] = data["x"]
            # diamonds[i]["y"] = data["y"]
            # diamonds[i]["z"] = data["z"]
            found = True
            break
    if found is False:
        return { "error": "diamond not found" }
    save_csv(diamonds)
    return diamonds


@app.route("/del_diamond/<int:id>", methods=['DELETE'])
def delete_diamond(id):
    df = pd.read_csv(CSV_FILE)
    df = df[df.ID != id]
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"message": "Diamond with id {} deleted.".format(id)})



@app.route("/clean")
def killthemall():
    save_csv([])
    return load_csv()



if __name__ == '__main__':
    app.run(debug=True)