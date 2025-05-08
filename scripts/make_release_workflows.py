import os.path
import jinja2

MATLAB_VERSIONS = [
    "R2020b",
    "R2021a",
    "R2021b",
    "R2022a",
    "R2022b",
    "R2023a",
    "R2023b",
    "R2024a",
    "R2024b",
]

jinja_env = jinja2.Environment(
    loader=jinja2.BaseLoader(),
    # use three braces to differentiate from github action double braces
    variable_start_string='{{{',
    variable_end_string='}}}',
)

this_dir = os.path.dirname(__file__)
template_path = os.path.join(this_dir, 'release-template.yml.jinja')
workflow_dir = os.path.join(this_dir, '..', '.github', 'workflows')

with open(template_path, 'r') as f:
    template = f.read()

for ver in MATLAB_VERSIONS:
    rendered = jinja_env.from_string(template).render(matlab_release=ver)
    workflow_path = os.path.join(workflow_dir, f'release-{ver.lower()}.yml')
    with open(workflow_path, 'w') as f:
        f.write(rendered)
