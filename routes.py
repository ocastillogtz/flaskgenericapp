import configparser
from flask import render_template,url_for
from form import generate_form_page,process_posted_form
from navbar import generate_navbar_html
from faq import generate_faq

def render_home(session="testing_session",request=""):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    my_app_name = config["APP_INFO"]["name"]
    my_short_description = config["APP_INFO"]["short_description"]
    if request:
        response = process_posted_form(request)
    else:
        response = ""
    return render_template("home.html",navbar=generate_navbar_html(),my_app_name=my_app_name,my_short_description=my_short_description, form=generate_form_page(), element_color=config["AESTHETICS"]["color_3"],response=response,logo_image_url=url_for("static",filename=config["AESTHETICS"]["logo"]))

def render_faq(session="testing_session",request=""):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    my_app_name = config["APP_INFO"]["name"]
    return render_template("faq.html",navbar=generate_navbar_html(), faq_content=generate_faq(), element_color=config["AESTHETICS"]["color_3"])




if __name__ == '__main__':
    print(render_home)