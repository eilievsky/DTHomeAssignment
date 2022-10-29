# main file. Contains Flask definition and endpoints
from flask import Flask , request
import appflow.flowfunctions as flowf

app = Flask(__name__)

@app.route("/status")
def get_status():
    return flowf.get_status()

@app.route("/deathsPeak")
def get_death_peak():
    args = request.args
    print(args)
    return flowf.get_death_peak(args_dict=args.to_dict())

@app.route("/provinceConfirmedMax")
def get_province_confirmed_max():
    return flowf.get_province_confirmed_max()


if __name__ == "__main__":
    app.run(debug=True)