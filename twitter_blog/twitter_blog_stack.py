from aws_cdk import (
    core,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_iam as iam
)


class TwitterBlogStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ########################## LAMBDA LAYERS #######################
        # Created layers directory and installed dependencies with
        # Example: $ pip install requests -t .
        twitterlayer = _lambda.LayerVersion(
            self, 'TwitterLayer',
            code = _lambda.AssetCode('layers/twitter'),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_7]
        )

        requestslayer = _lambda.LayerVersion(
            self, 'RequestsLayer',
            code = _lambda.AssetCode('layers/requests'),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_7]
        )

        bs4layer = _lambda.LayerVersion(
            self, 'Bs4Layer',
            code = _lambda.AssetCode('layers/bs4'),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_7]
        )

        ################### LAMBDA ##############################
        tweet_lambda = _lambda.Function(
            self, 'TweetHandler',
            runtime = _lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='handler.main',
            timeout=core.Duration.seconds(300),
            layers=[twitterlayer, requestslayer, bs4layer]
        )

        # Add permissions to get the SSM parameters for Twitter API keys
        tweet_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=['*'],
            actions=['ssm:GetParameters','logs:CreateLogGroup','logs:CreateLogStream', 'logs:PutLogEvents']
        ))

        # CloudWatch rule that runs every Friday at 6pm 
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='FRI',
                year='*'
            )
        )

        # Add CW rule as event source to Lambda function
        rule.add_target(targets.LambdaFunction(tweet_lambda))
