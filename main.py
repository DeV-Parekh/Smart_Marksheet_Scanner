import re
import sqlite3

import easyocr
import numpy as np
from flask import Flask, flash, redirect, render_template, request
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(["pdf"])

PATH = "" # your project path
POPPLER_PATH = "" # your poppler bin path

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def gseb(path):
    connection_obj = sqlite3.connect('marks.db')
    cursor_obj = connection_obj.cursor()

    cursor_obj.execute("DROP TABLE IF EXISTS MARKS")

    table = """ CREATE TABLE MARKS (
        			Subject VARCHAR(255) NOT NULL,
        			Mark INT NOT NULL
        		); """

    cursor_obj.execute(table)

    print("Table is Ready")
    subjects = ["ENGLISH", "SOCIAL SCIENCE", "SCIENCE AND TECHNOLOGY", "MATHEMATICS", "GUJARATI", "SANSKRIT", "TOTAL"]
    reader = easyocr.Reader(['en'])

    images = convert_from_path(path,
                               poppler_path=POPPLER_PATH)

    bounds = reader.readtext(np.array(images[0]), min_size=0, slope_ths=0.2, ycenter_ths=0.7, height_ths=0.6,
                             width_ths=0.8, decoder='beamsearch', beamWidth=10)
    text = ''
    for i in range(len(bounds)):
        text = text + bounds[i][1] + '\n'

    lines = re.split(r'\n| ', text)

    sub_re = re.compile(r'^\d\d\s\D')
    marks_re = re.compile(r'^\d\d\d$')

    marks = []
    result = []

    for line in lines:
        if sub_re.search(line) or marks_re.search(line):
            marks.append(line)

    marks = list(map(int, marks[len(marks) - 7:]))
    marks_u = list(map(int, marks[len(marks) - 7:-1]))
    if sum(marks_u) == marks[-1]:
        for subject, mark in zip(subjects, marks):
            result.append({'subject': subject, 'marks': mark})
            cursor_obj.execute('''INSERT INTO MARKS VALUES (?, ?)''', (subject, mark))
        result.append({"subject": "TOTAL MAXIMUM MARKS", "marks": "600"})
        cursor_obj.execute('''INSERT INTO MARKS VALUES ('Total Maximum Marks', '600')''')
        connection_obj.commit()

        data = cursor_obj.execute('''SELECT * FROM MARKS''')
        for row in data:
            print(row)

        connection_obj.close()
        return result
    else:
        return [{'subject': 'Invalid', 'marks': 'Please upload again'}]


def cbse(path):
    connection_obj = sqlite3.connect('marks.db')
    cursor_obj = connection_obj.cursor()

    cursor_obj.execute("DROP TABLE IF EXISTS MARKS")

    table = """ CREATE TABLE MARKS (
           			Subject VARCHAR(255) NOT NULL,
           			Mark INT NOT NULL
           		); """

    cursor_obj.execute(table)

    print("Table is Ready")

    reader = easyocr.Reader(['en'])

    images = convert_from_path(path,
                               poppler_path=POPPLER_PATH)

    bounds = reader.readtext(np.array(images[0]), min_size=0, slope_ths=0.2, ycenter_ths=0.7, height_ths=0.6,
                             width_ths=0.8, decoder='beamsearch', beamWidth=10)

    text = ''
    for i in range(len(bounds)):
        text = text + bounds[i][1] + '\n'

    lines = re.split(r'\n| ', text)
    marks_re = re.compile(r'^\d\d\d$')
    result = []
    for line in lines:
        if marks_re.search(line):
            if int(line) <= 101:
                result.append(line)

    subjects = ["ENGLISH COMM", "HINDI COURSE-A", "MATHEMATICS", "SCIENCE", "SOCIAL SCIENCE", "TOTAL OBTAINED MARKS"]
    result_updated = []
    mark_list = []
    i = 0
    isCorrect = True

    while True:
        if len(mark_list) == 5:
            break
        i += 1
        j = i + 1
        k = j + 1
        if int(result[i]) + int(result[j]) == int(result[k]):
            mark_list.append(result[k])
            i = k + 1
        else:
            isCorrect = False
            break

    # print(mark_list)
    mark_list = list(map(int, mark_list))
    total = sum(mark_list)
    mark_list.append(total)

    if isCorrect:
        for subject, mark in zip(subjects, mark_list):
            result_updated.append({'subject': subject, 'marks': mark})
            cursor_obj.execute('''INSERT INTO MARKS VALUES (?, ?)''', (subject, mark))
        connection_obj.commit()
        connection_obj.close()
        return result_updated

    return [{'subject': 'Invalid', 'marks': 'Please upload again'}]

@app.route("/")
def upload_form():
    return render_template("board.html")


@app.route("/upload")
def index():
    return render_template("upload.html")

@app.route("/upload2")
def index2():
    return render_template("upload2.html")

@app.route("/index")
def upload():
    return render_template("index.html")


@app.route("/upload_gseb", methods=["POST"])
def upload_gseb():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected for uploading")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{PATH}/Images/" + filename)
            result = gseb(f"{PATH}/Images/" + filename)
            with open(f"{PATH}/static/data.json", 'w') as file:
                file.write(str(result).replace("'", '"'))

            flash("File successfully uploaded")
            return redirect("/index")
        else:
            flash("Allowed file types are pdf")
            return redirect(request.url)

@app.route("/upload_cbse", methods=["POST"])
def upload_cbse():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected for uploading")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{PATH}/Images/" + filename)
            result = cbse(f"{PATH}/Images/" + filename)
            with open(f"{PATH}/static/data.json", 'w') as file:
                file.write(str(result).replace("'", '"'))

            flash("File successfully uploaded")
            return redirect("/index")
        else:
            flash("Allowed file types are pdf")
            return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
