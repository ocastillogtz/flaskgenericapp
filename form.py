import configparser
import time
import random
import logging
from email_stuff import send_email,make_email_content
from flask import render_template

AVAILABLE_FORM_ELEMENTS_DICT = {"upload_input" : ["name","label"],
                                "email_input" : ["name","label"],
                                "password_input" : ["name","label"],
                                "confirm_checkbox" : ["name","message","warning"],
                                "shottext_input" : ["name","label"],
                                "radio_buttons_input" : ["radio_title","radios"],
                                "textarea_input" : ["name","label","prefilled"]
                                }

def generate_form_page(session="testing_session"):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    form = """<form action="/home" method="GET" enctype="multipart/form-data">\n<input type="hidden" id="form_1" name="form_1" value="process_1">"""
    for item in config["FORM"]:
        if config["FORM"][item]:
            element_parameters = config["FORM"][item].split(",")
            if element_parameters[0] in AVAILABLE_FORM_ELEMENTS_DICT:
                content = {}
                for i in range(1,len(element_parameters)):
                    param_list = AVAILABLE_FORM_ELEMENTS_DICT[element_parameters[0]]
                    content[param_list[i-1]] = element_parameters[i]

                html_fragment = render_template(element_parameters[0] + ".html",content=content)
                form = form + html_fragment


    form = form + """
    <button type="submit" class="btn btn-dark" style="padding : 10px">Submit</button>
    </form>\n"""
    return form


def process_posted_form(request):
    response = ""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    if request.form:
        # _# check if there is a file
        if "up_file" in request.files:
            uploaded_file = request.files['up_file']
            # _# check that the file has a name
            if uploaded_file.filename != '':
                if uploaded_file.filename.endswith(config["FILE_CHARACTERISTICS"]["extension"]):
                    # _#_# Change the name for data protection purposes
                    # _# Get the unix epoch and remove the numbers after the "."
                    timestamp = str(time.time()).split(".")[0]
                    # _# generates a string composed of 8 character numbers from 0 to 9
                    id_randomly_assigned = str(random.randint(0, 99999999)).zfill(8)
                    # _# Reassign name to file
                    new_name_uploaded_file = timestamp + id_randomly_assigned
                    uploaded_file.filename = new_name_uploaded_file
                    # _# download_file
                    try:
                        uploaded_file.save(uploaded_file.filename)
                    except:
                        print("There was something wrong with that file")
                    # _# check if file is in the working directory
                    try:
                        just_uploaded_file = open(new_name_uploaded_file, "r")
                        file_upload_confirmation = True
                    except:
                        print("couldn't find the file")
                        file_upload_confirmation = False

                    if "email" in request.form and file_upload_confirmation:
                        text = make_email_content(request.form['email'])
                        try:
                            send_email(request.form['email'], "Confirmation of task initiation", text)
                            response = "In a moment you are going to receive an email confirmation"
                        except Exception as e:
                            response = "the email sending fail due to: {e}".format(e=e)
                        return response
                    else:
                        response = "Error, you must provide a file and an email."
                        logging.error(response)
                        return response
                else:
                    response = "the file is not a {extension} file".format(extension=config["FILE_CHARACTERISTICS"]["extension"])
                    logging.error(response)
                    return response
            else:
                response = "File must have a name"
                logging.error(response)
                return response
        else:
            response = "There's no upload file"
            logging.error(response)
            return response
    else:
        response = "The posted form is empty"
        logging.error(response)
        return response



if __name__ == '__main__':
    generate_form_page()