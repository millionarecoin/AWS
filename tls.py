import boto3
from botocore.exceptions import ClientError

region = 'us-east-1'


def lambda_handler(event, context):
    print('1')
    version = '1-2'
    try:
        lb_type = 'alb'
        if lb_type == 'alb':
            elb = boto3.client('elbv2', region_name=region)
            name = 'LoadBalancers'
            print('alb')
        else:
            print('no alb found')
    except Exception as exc:
        print('exception hitting')
        exit(1)
    bals = elb.describe_load_balancers()
    load_balancer_arn = bals['LoadBalancers'][0]['LoadBalancerArn']
    print('bals')
    print(bals)
    attrib = elb.describe_load_balancer_attributes(LoadBalancerArn=load_balancer_arn)
    print('attributes')
    print(attrib)

    policy = elb.describe_listeners(LoadBalancerArn=load_balancer_arn)

    print('policy')
    print(policy)

    tls = policy['Listeners'][0]['SslPolicy']
    print('tls: ', tls)
    if version in tls:
        print('this alb has version 1-2')
        send_email()


def send_email():
    SENDER = "Sender Name <sender@example.com>"
    RECIPIENT = "recipient@example.com"
    CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = region

    # The subject line for the email.
    SUBJECT = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )

    # The HTML body of the email.
    BODY_HTML = """<html>
 <head></head>
 <body>
   <h1>Amazon SES Test (SDK for Python)</h1>
   <p>This email was sent with
     <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
     <a href='https://aws.amazon.com/sdk-for-python/'>
       AWS SDK for Python (Boto)</a>.</p>
 </body>
 </html>
            """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
