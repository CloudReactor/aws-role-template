import argparse
import json
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()

parser.add_argument('--environment',
                    help='CloudReactor deployment environment')

args = parser.parse_args()

deployment_environment = args.environment

user_suffix = ''
if deployment_environment and (deployment_environment != 'production'):
    user_suffix = "_" + deployment_environment

env = Environment(
    loader=FileSystemLoader('./')
)

template = env.get_template('cloudreactor-aws-role-template.json.j2')

with open('url_requester.py', 'r') as f:
    url_requester_contents = f.read()

data = {
  'url_requester_contents': json.dumps(url_requester_contents),
  'user_suffix': user_suffix

}

output = template.render(data)

output_filename = f"cloudreactor-aws-role-template{user_suffix.replace('_', '.')}.json"

with open(output_filename, 'w') as f:
    f.write(output)

print(f"Wrote file '{output_filename}' with CloudFormation template.")
