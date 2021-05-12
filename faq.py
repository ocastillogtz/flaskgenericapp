import configparser
from flask import render_template

def generate_faq():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    elements = []
    for enumeration,item in enumerate(config["FAQ"]):
        if config["FAQ"][item]:
            title,body = config["FAQ"][item].split("_-_")
            elements.append((str(enumeration),title,body))

    html_fragment = render_template("accordion_element.html",elements=elements)
    return html_fragment