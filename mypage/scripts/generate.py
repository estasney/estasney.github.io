from jinja2 import Template
import json


def get_template(fp):
    with open(fp, "r") as html_file:
        return Template(html_file.read())


def get_data(fp):
    with open(fp, 'r') as json_file:
        return json.load(json_file)


template = get_template(r"C:\Users\estasney\PycharmProjects\pages\mypage\templates\template.html")
data = get_data(r"C:\Users\estasney\PycharmProjects\pages\mypage\data\me.json")
output = template.render(basics=data['basics'], skills=data['skills'], work=data['work'],
                         educations=data['education'], awards=data['awards'], projects=data['projects'],
                         interests=data['interests'])
with open(r"C:\Users\estasney\PycharmProjects\pages\index.html", "w+") as html_file:
    html_file.write(output)
