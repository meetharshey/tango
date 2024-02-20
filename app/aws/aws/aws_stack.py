from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambdas,
    aws_events as events,
    aws_events_targets as targets,

)

from constructs import Construct
from aws_cdk.aws_lambda import LayerVersion, AssetCode
from constructs import Construct

class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TestCdKpythonQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        with open("index.py", encoding="utf8") as fp:
            handler_code = fp.read()


        role = iam.Role(
            self, 'myappRole',
            assumed_by= iam.ServicePrincipal('lambda.amazonaws.com'))

        role.add_to_policy(iam.PolicyStatement(
            effect = iam.Effect.ALLOW,
            resources = ["*"],
            actions= ['events:*']))

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["arn:aws:iam::*:role/AWS_Events_Invoke_Targets"],
            actions=['iam:PassRole']))

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]))

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["s3:*"]))

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["lambda:*"]))

        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["sns:*"]))

        lambdaFn = lambdas.Function(
            self, "Singleton",
            code=lambdas.InlineCode(handler_code),
            handler="index.lambda_handler",
            timeout=Duration.seconds(600),
            runtime=lambdas.Runtime.PYTHON_3_8,
            memory_size=512,
            environment=dict(PATH="/opt"),
            role = role
        )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='59',
                hour='6-20/4',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))

        ac = AssetCode("./python")

        layer = LayerVersion(self, "mytestapp", code=ac,
                             description="test app layer",
                             compatible_runtimes=[lambdas.Runtime.PYTHON_3_8],
                             layer_version_name='test-layer')
        lambdaFn.add_layers(layer)
