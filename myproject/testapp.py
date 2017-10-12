from functools import wraps, partial
import advutil as adv

from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)

advinfo = adv.AdviserInfo()

@app.route("/adviserinfo")
def advindex():
    return render_template('adviserinfo_index.html',
        title = "AdviserInfo",
        fields = advinfo.idxtable_df.columns)

@app.route("/data")
def data():
    return jsonify(advinfo.idxtable_ajax)

@app.route("/secfilings")
def secindex():
    return render_template('adviserinfo_index.html', title = "SEC Filings")

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded=True, debug = 1, port = 8000)
    request.data
