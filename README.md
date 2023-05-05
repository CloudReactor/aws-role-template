# aws-role-template

![Tests](https://github.com/CloudReactor/aws-role-template/workflows/Tests/badge.svg?branch=master)

This project contains two CloudFormation templates that can be used to set up CloudReactor in your AWS account.

1. [Allowing CloudReactor to manage your ECS tasks and AWS Lambda functions](#allowing-cloudreactor-to-manage-your-tasks):
If you did NOT use the [AWS Setup Wizard](https://github.com/CloudReactor/cloudreactor-aws-setup-wizard), i.e. you want to [set up CloudReactor manually](https://docs.cloudreactor.io/manual_setup.html#optional-set-aws-role-permissions-to-allow-cloudreactor-to-stop-start-and-schedule-ecs-tasks), this role template must be installed to allow CloudReactor to start your ECS tasks or Lambda functions.
2. [Deployer policy](#deployer-policy-role-and-user): If you arrived here after following the CloudReactor [Getting Started](https://docs.cloudreactor.io/#optional-setting-up-a-new-aws-user-with-deployment-permissions) guide, this will let you create a special user and role that has the minimum permissions required to deploy tasks to ECS. Once this user / role is created, you can enter the credentials into the CloudReactor quickstart repo configuration file at `deploy/docker_deploy.env`. CloudReactor will then assume this role when deploying tasks.

## Allowing CloudReactor to manage your ECS tasks and Lambda functions

Installing this template is only required if you want to use CloudReactor to
manage your ECS tasks and Lambda functions, but want to complete setup manually
(i.e. you don't want to use the CloudReactor
[AWS Setup Wizard](https://docs.cloudreactor.io/#set-up-aws-infrastructure-link-to-cloudreactor)).
If you've used the AWS Setup Wizard, you can ignore this section!

1. In the AWS console, go to CloudFormation. Ensure you are in the AWS region
you want to run your tasks in. You can change the region by selecting the
Region dropdown in the top right menu bar.
2. In the Stacks section, click the "Create Stack" button and select "With new resources (standard)"
3. In the "Prerequisite - Prepare Template" section, choose "Template is ready"
4. In the "Specify template" section, choose "Amazon S3 URL" (which should be selected by default).
In the "Amazon S3 URL" field, enter:

    https://cloudreactor-customer-setup.s3-us-west-2.amazonaws.com/cloudreactor-aws-role-template-1.json

5. Hit the "Next" button
6. In the "Stack name" section, enter a name like "CloudReactor"
7. In the parameters section, under "ExternalId", enter a randomly generated ID that will be used
to limit access to the roles.
We'll use this key when filling in the ExternalId value when creating
a Run Environment in the CloudReactor dashboard, so write it down. To generate an ID, you could use a generator like [1password](https://1password.com/password-generator/); a 16-digit key is fine. For more information, see
[How to Use an External ID When Granting Access to Your AWS Resources to a Third Party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).
8. Also the parameters section, under "WorkflowStarterAccessKey", enter another randomly generated ID that will be used
to validate requests from Cloudwatch to start Workflows on a schedule. Again, we'll use this key when filling in the
"Workflow Starter Lambda ARN" field when creating a Run Environment in the CloudReactor dashboard, so write it down.
9. On the next page, you may enter tags for the stack, but it is not required.
All other options on the page are also not required. Hit the "Next" button
after entering any options.
10. On the final page, check the checkbox at the bottom that acknowledges
that CloudFormation may create IAM resources, and hit "Create Stack".
11.  It will take a few minutes for the stack to be created. Once this is done, select the stack and go to the "Outputs" tab.
Note the values of the "CloudreactorRoleARN", "TaskExecutionRoleARN",
and "WorkflowStarterARN" keys, to be entered when creating a Run Environment
in CloudReactor. You can return to the CloudReactor Quick Start guide now!

If you want to run tasks in multiple AWS regions, repeat these steps for
each desired region. First change the region in the top right menu
bar, then redo the steps above.

## Deployer policy, role, and user

The CloudFormation template `cloudreactor-aws-deploy-role-template.json` creates a policy containing the permissions required to deploy tasks to ECS, as well as a role and user that use that policy. The user created is named "cloudreactor-deployer". The user's access key ID and access key secret will be shown in the AWS console.
Note that you don't need to deploy this template if you can use a user or role that is able to deploy tasks to ECS, such as an admin user.

To install the template and create these resources:

1. In the AWS console, go to CloudFormation. Note that the region doesn't matter as we are creating IAM resources.
2. In the Stacks section, click the "Create Stack" button and select "With new resources (standard)"
3. In the "Prerequisite - Prepare Template" section, choose "Template is ready"
4. In the "Specify template" section, choose "Amazon S3 URL" (which should be selected by default).
In the "Amazon S3 URL" field, enter:

    https://cloudreactor-customer-setup.s3-us-west-2.amazonaws.com/cloudreactor-aws-deploy-role-template.json

5. Hit the "Next" button
6. In the "Stack name" section, enter a name like "CloudReactor-deployer"
7. On the next page, you may enter tags for the stack, but it is not required.
All other options on the page are also not required. Hit the "Next" button
after entering any options.
8. On the final page, check the checkbox at the bottom that acknowledges
that CloudFormation may create IAM resources, and hit "Create Stack".
9. After the stack is created, select the stack and go to the "Outputs" tab. You can now use the CloudreactorDeployerAccessKeyId value as the access key
(AWS_ACCESS_KEY_ID environment variable) and the CloudreactorDeployerAccessKeySecret value as the secret key (AWS_SECRET_ACCESS_KEY environment variable) in the CloudReactor quickstart repo configuration file at `deploy.env`.

# Using the Access Keys

The values of `CloudreactorDeployerAccessKeyId` and
`CloudreactorDeployerAccessKeySecret` in the stack output
can be used to set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment
variables respectively.

These can be entered into the CloudReactor config file at `deploy.env` or,
stored in your AWS configuration using `aws configure`
if using
the [CloudReactor ECS deployer Docker image and driver script](https://github.com/CloudReactor/aws-ecs-cloudreactor-deployer).

Alternatively you can save these values in [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
if deploying with [CloudReactor ECS deployer GitHub action](https://github.com/marketplace/actions/cloudreactor-aws-ecs-deployer).

# Using the Created Role

If you don't want to use access keys, you can use the role that is output.
There are two ways of using the role:

1. Assign the role to an EC2 instance used to deploy tasks. This EC2
instance can speed up deployments because it is deployed in Amazon's network,
so pushing images is much faster than doing it from developer machines.
See [IAM Roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) for instructions on how to assign
roles to EC2 instances.
2. Allow the role to be assumed by other users, which may include developers,
machine users, or groups. If you use AWS Directory Service, you can assign the role to users using the Directory Service directly. Otherwise,
add an AssumeRolePolicyDocument to the CloudReactor deployer role allowing the user to assume the role,
and add permission for the user to assume the role. See [Assigning Roles to Users](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/assign_role.html) for detailed instructions.
