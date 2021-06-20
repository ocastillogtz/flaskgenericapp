"""
This is a Flask website template for a web tool or whatever
"""
import logging
import configparser
from waitress import serve
from flask import Flask, render_template, url_for,redirect,request
from routes import render_home, render_faq, render_generic_page, process_client_data,render_show_job

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.args:
        if request.args["form_1"] == "process_1":
            form_data = request.args
            job_id = process_client_data(form_data)
            return redirect("/job_id={job_id}".format(job_id=str(job_id)))
        else:
            return render_home(session="testing_session")
    else:
        return render_home(session="testing_session")

@app.route('/job_id=<int:job_id>', methods=['GET'])
def show_job(job_id):
    return render_show_job(job_id)

@app.route('/faq', methods=['GET'])
def faq():
    if request.method == 'POST':
        return render_faq(session="testing_session", request=request)
    else:
        return render_faq(session="testing_session")

@app.route('/', methods=['GET', 'POST'])
def initial():
    return redirect("/home")

@app.route('/generic_page', methods=['GET'])
def generic_page():
    return render_generic_page(session="testing_session")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    logging.basicConfig(filename='mywebapp.log', level=logging.DEBUG)
    app.secret_key = config["APP_INFO"]["secret_key"]
    serve(app, host='127.0.0.1', port=5000)
