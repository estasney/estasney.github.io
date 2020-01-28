from jinja2 import Environment, PackageLoader, select_autoescape
import json

flatten = lambda x: [item for sublist in x for item in sublist]


def get_template(fp):
    with open(fp, "r") as html_file:
        return Template(html_file.read())


def get_data(fp):
    with open(fp, 'r') as json_file:
        return json.load(json_file)


def remove_duplicate_skills(skills, skills_ul):
    # prevent skills that appear as keywords in skills from appearing in the unordered list below
    seen = set(flatten([skill_group['keywords'] for skill_group in skills]))

    skills_ul = [skill for skill in skills_ul if skill not in seen]
    return skills_ul


env = Environment(
        loader=PackageLoader('mypage', 'templates'),
        autoescape=select_autoescape(['html'])
        )

template = env.get_template("so_template.html")
data = get_data("/home/eric/PycharmProjects/MyPage/mypage/data/me.json")
skills, skills_ul = data['skills'], data['skills_ul']
skills_ul = remove_duplicate_skills(skills, skills_ul)
output = template.render(basics=data['basics'], skills=skills, skills_ul=skills_ul, work=data['work'],
                         educations=data['education'], awards=data['awards'], projects=data['projects'],
                         interests=data['interests'])
with open("/home/eric/PycharmProjects/MyPage/index.html", "w+") as html_file:
    html_file.write(output)
