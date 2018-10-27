from jinja2 import Template
import json


def get_template(fp):
    with open(fp, "r") as html_file:
        return Template(html_file.read())


def get_data(fp):
    with open(fp, 'r') as json_file:
        return json.load(json_file)


template = get_template('/home/eric/PycharmProjects/MyPage/mypage/templates/template.html')
data = get_data('/home/eric/PycharmProjects/MyPage/mypage/data/me.json')
output = template.render(basics=data['basics'], skills=data['skills'], work=data['work'],
                         educations=data['education'], awards=data['awards'], projects=data['projects'],
                         interests=data['interests'])
with open(r"/home/eric/PycharmProjects/MyPage/index.html", "w") as html_file:
    html_file.write(output)
