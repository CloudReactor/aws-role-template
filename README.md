# aws-role-template
A CloudFormation template that allows oneprocdash to run processes for customers.
It also creates a role to run ECS tasks with support for Cloudwatch logs.

## Installation

1. In the AWS console, go to CloudFormation.
2. In the Stacks section, click the "Create Stack" button.
3. In the "Prerequisite - Prepare Template" section, choose "Template is ready"
4. In the "Specify template" section, choose "Upload a template file"
5. Click the "Choose file" button and select the "oneprocdash-aws-role-template.json" file
6. Hit the "Next" button
7. In the "Stack name" section, enter a name like "Oneprocdash"
8. In the parameters section, under "ExternalId", enter a randomly generated ID that will be used
to limit access to the roles. Use this key when filling in the ExternalId value when creating
a Run Environment in oneprocdash. For more information, see
[How to Use an External ID When Granting Access to Your AWS Resources to a Third Party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).
9. Also the parameters section, under "WorkflowStarterAccessKey", enter another randomly generated ID that will be used
to validate requests from Cloudwatch to start Workflows on a schedule. Use this key when filling in the 
"Workflow Starter Lambda ARN" field when creating a Run Environment.
10. On the next page, you may enter tags for the stack, but it is not required.
All other options on the page are also not required. Hit the "Next" button
after entering any options.
11. On the final page, check the checkbox at the bottom that acknowledges
that CloudFormation may create IAM resources, and hit "Create Stack".
12. After the stack is created, select the stack and go to the "Outputs" tab.
Note the values of the "OneprocdashRoleARN", "TaskExecutionRoleARN",
and "WorkflowStarterARN" keys, to be entered when creating a Run Environment
in oneprocdash. See https://processes.oneprocdash.com/run_environments to create
and edit your Run Environments.
