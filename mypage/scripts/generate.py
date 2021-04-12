from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
import os
import argparse
import dotenv
import click


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


def get_contact_info():
    """
    Prompt for contact info I want to leave out of VCS
    """
    contacts = []
    while True:
        try:
            contact = input("Enter Contact [blank to stop]")
            if not contact:
                return contacts
            contacts.append(contact)
        except KeyboardInterrupt:
            return contacts


@click.command()
@click.option("-c", "--contacts", type=bool, default=False, help="Manually Enter Contact Information")
@click.option("-t", "--template", type=click.Choice(["stx", "simple"]), default="stx", help="Select Template")
def generate(contacts, template):
    dotenv.load_dotenv()
    env = Environment(
            loader=PackageLoader('mypage', 'templates'),
            autoescape=select_autoescape(['html'])
            )

    contact_info = get_contact_info() if contacts else None
    template = env.get_template(f"{template}.html")
    data_path = os.path.join(os.pardir, "data", "me.yml")
    data = get_data(data_path)
    skills, skills_ul = data['skills'], data['skills_ul']
    skills_ul = remove_duplicate_skills(skills, skills_ul)
    output = template.render(basics=data['basics'], skills=skills, skills_ul=skills_ul, work=data['work'],
                             educations=data['education'], projects=data['projects'],
                             interests=data['interests'], contact_info=contact_info,
                             highlights=data['highlights'], technologies=data['technologies'],
                             env=os.environ)

    file_name = "index-contact.html" if contacts else "index.html"
    file_path = os.path.join(os.pardir, os.pardir, file_name)
    with open(file_path, "w+", encoding="utf-8") as html_file:
        html_file.write(output)


if __name__ == '__main__':
    generate()
