import argparse
import json
from jinja2 import Environment, FileSystemLoader


parser = argparse.ArgumentParser()

parser.add_argument('--environment',
                    help='CloudReactor deployment environment')

parser.add_argument('--domain-suffix',
                    help='Domain restriction for Workflow Starter Lambda request URLs that point to CloudReactor API endpoints. Should normally start with a ".". Defaults to ".cloudreactor.io"')

parser.add_argument('--output-filename-qualifier',
                    help='Output filename qualifier. The output file will be named cloudreactor-aws-role-template.{qualifier}.json. Defaults to a "." followed by the environment name.')

args = parser.parse_args()

deployment_environment = args.environment

role_suffix = ''
if deployment_environment and (deployment_environment != 'production'):
    role_suffix = "_" + deployment_environment

domain_suffix = args.domain_suffix or '.cloudreactor.io'


env = Environment(
    loader=FileSystemLoader('./src/jinja2')
)

template = env.get_template('cloudreactor-aws-role-template.json.j2')

with open('src/python/url_requester.py', 'r') as f:
    url_requester_contents = f.read()

data = {
  'url_requester_contents': json.dumps(url_requester_contents),
  'role_suffix': role_suffix,
  'domain_suffix': json.dumps(domain_suffix)
}

output = template.render(data)

try:
    json.loads(output)
except Exception as ex:
    print("Generated template is not valid JSON!")
    raise ex

if args.output_filename_qualifier:
    qualifier = '.' + args.output_filename_qualifier
else:
    qualifier = role_suffix.replace('_', '.')

output_filename = f"cloudreactor-aws-role-template{qualifier}.json"

with open(output_filename, 'w') as f:
    f.write(output)

print(f"Wrote file '{output_filename}' with CloudFormation template.")
