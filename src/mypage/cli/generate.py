import os
from datetime import date
from functools import partial
from typing import Literal

import click
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from mypage.models import Resume
from mypage.settings import get_settings


def format_date(value: date | Literal["present"] | None, format_str: str = "%b %Y") -> str:
    """Format a date for display in templates.
    
    Args:
        value: The date value to format
        format_str: The strftime format string (default: "%b %Y" for "Nov 2025")
    """
    match value:
        case None:
            return ""
        case str() if value == "present":
            return "Present"
        case date():
            return value.strftime(format_str)
        case _:
            msg = f"Unsupported date value: {value!r}"
            raise ValueError(msg)



@click.command()
@click.option(
    "-c",
    "--contacts",
    type=bool,
    default=False,
    help="Include Contact Information from .env",
)
@click.option(
    "-t",
    "--template",
    type=click.Choice(["stx", "simple"]),
    default="stx",
    help="Select Template",
)
def generate(contacts: bool, template: Literal["stx", "simple"])-> None:
    
    env = Environment(
        loader=PackageLoader("mypage", "templates"),
        autoescape=select_autoescape(["html"]),
    )
    env.filters['format_date'] = format_date
    env.filters['format_date_year'] = partial(format_date, format_str="%Y")
    env.filters['format_date_month_year'] = partial(format_date, format_str="%b %Y")
    settings = get_settings()
    contact_info = settings.info if contacts else None
    template_obj = env.get_template(f"{template}.html")
    
    resume = Resume.model_validate(yaml.load(settings.me_file.read_text(encoding="utf-8"), Loader=yaml.SafeLoader))
    output = template_obj.render(
        basics=resume.basics,
        skills=resume.skills,
        skills_ul=resume.skills_ul,
        work=resume.work,
        educations=resume.education,
        projects=resume.projects,
        interests=resume.interests,
        contact_info=contact_info,
        highlights=resume.highlights,
        technologies=resume.technologies,
        env=os.environ,
    )
    
    click.echo(output)

    file_name = "index-contact.html" if contacts else "index.html"
    (settings.repo_root / file_name).write_text(output, encoding="utf-8")
    


if __name__ == "__main__":
    generate()
