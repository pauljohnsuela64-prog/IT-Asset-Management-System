from flask import Flask, render_template

from asset_repository import get_all_assets


app = Flask(__name__)


@app.route("/")
def home():
    assets = get_all_assets()
    return render_template("assets.html", assets=assets)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)