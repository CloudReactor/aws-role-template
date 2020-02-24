import json
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('./')
)

template = env.get_template('cloudreactor-aws-role-template.json.j2')

with open('url_requester.py', 'r') as f:
    url_requester_contents = f.read()

data = {
  'url_requester_contents': json.dumps(url_requester_contents)
}

output = template.render(data)

output_filename = 'cloudreactor-aws-role-template.json'

with open(output_filename, 'w') as f:
    f.write(output)

print(f"Wrote file '{output_filename}' with CloudFormation template.")
