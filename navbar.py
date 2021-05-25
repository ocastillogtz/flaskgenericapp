import configparser
from flask import render_template,url_for

def generate_navbar_html(session="testing_session"):
    """
    Generates the navigation bar div for the website. It uses the bootstrap framework, you can learn more about
    navbars in https://getbootstrap.com/docs/4.0/components/navbar/
    :param session:
    :return: A HTML rendering made from jinja2, ready to be shown in our website
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    tabs_simple = []
    tabs_cascades = []
    #_# Here we are going to check in the settings file, which are the tabs and what kind of tabs they are.
    for item in config["TABS"]:
        if config["TABS"][item]:
            cascade = []
            for sub_item, sub_ref_name in zip(config["TABS"][item].split(","), config["TABS_LINK_TO"][item].split(",")):
                cascade.append((sub_ref_name, sub_item))
            tabs_cascades.append((config["TABS_DEFAULT_STATE"][item], "", item, cascade))
        else:
            tabs_simple.append((config["TABS_DEFAULT_STATE"][item], config["TABS_LINK_TO"][item], item))
    #_# we add as parameters more characteristics from te settings file, such as the logo, the font color, the background color.
    return render_template("navbar.html",
                           tabs_cascades=tabs_cascades,
                           logo_image_url=url_for("static",filename=config["AESTHETICS"]["logo"]),
                           tabs_simple=tabs_simple,app_name=config["APP_INFO"]["name"],
                           light_or_dark=config["AESTHETICS"]["navbar_light_or_dark"],
                           navbar_background_color=config["AESTHETICS"]["navbar_background_color"],
                           body_background=config["AESTHETICS"]["color_2"])



if __name__ == '__main__':
    generate_navbar_html()