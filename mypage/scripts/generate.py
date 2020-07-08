from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import os


def flatten(coll):
    """From one of my favorite StackOverflow answers
    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists/952952#952952
    """
    return [item for sublist in coll for item in sublist]


def remove_duplicate_skills(skills, skills_ul):
    # prevent skills that appear as keywords in skills from appearing in the unordered list below
    seen = set(flatten([skill_group['keywords'] for skill_group in skills]))

    skills_ul = [skill for skill in skills_ul if skill not in seen]
    return skills_ul


def get_data(fp):
    with open(fp, 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)


env = Environment(
        loader=PackageLoader('mypage', 'templates'),
        autoescape=select_autoescape(['html'])
        )

if __name__ == '__main__':
    template = env.get_template("so_template.html")
    data_path = os.path.join("..", "data", "me.yml")
    data = get_data(data_path)
    skills, skills_ul = data['skills'], data['skills_ul']
    skills_ul = remove_duplicate_skills(skills, skills_ul)
    output = template.render(basics=data['basics'], skills=skills, skills_ul=skills_ul, work=data['work'],
                             educations=data['education'], awards=data['awards'], projects=data['projects'],
                             interests=data['interests'])

    page_out = os.path.join("..", "..", "index.html")
    with open(page_out, "w+") as html_file:
        html_file.write(output)