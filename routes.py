import configparser
from flask import render_template,url_for
from form import generate_form_page,process_posted_form
from navbar import generate_navbar_html
from faq import generate_faq

def render_home(session="testing_session",request=""):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    if request:
        response = process_posted_form(request)
    else:
        response = ""
    return render_template("home.html",
                           navbar=generate_navbar_html(),
                           my_app_name=config["APP_INFO"]["name"],
                           my_short_description=config["APP_INFO"]["short_description"],
                           form=generate_form_page(),
                           element_color=config["AESTHETICS"]["color_3"],
                           response=response,
                           logo_image_url=url_for("static",filename=config["AESTHETICS"]["logo"]))

def render_faq(session="testing_session",request=""):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    my_app_name = config["APP_INFO"]["name"]
    return render_template("faq.html",
                           navbar=generate_navbar_html(),
                           faq_content=generate_faq(),
                           element_color=config["AESTHETICS"]["color_3"])

def render_generic_page(session="testing_session",request=""):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    sections_content = []
    for i in range(1, 21):
        section_name = "section_" + str(i)
        if section_name in config["GENERIC"]:
            print(config["GENERIC"][section_name])
            sections_content.append(config["GENERIC"][section_name])
        else:
            break

    return render_template("generic_page.html",
                                    navbar=generate_navbar_html(),
                                    title=config["GENERIC"]["title"],
                                    sections_content=sections_content,
                                    end=config["GENERIC"]["end"])


if __name__ == '__main__':
    print(render_home)