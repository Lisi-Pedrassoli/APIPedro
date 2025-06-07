import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Dados do e-mail - idealmente, viria no event, aqui exemplo fixo
    SENDER = "lisi1809.net@gmail.com"
    RECIPIENT = "lisi1809.net@gmail.com"
    AWS_REGION = "us-east-2"  # Ajuste conforme sua região SES
    
    SUBJECT = "Email enviado pela AWS Lambda"
    BODY_TEXT = "Este é um e-mail simples enviado pela função Lambda usando Amazon SES."
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Email enviado pela AWS Lambda</h1>
      <p>Este é um e-mail simples enviado pela função Lambda usando <b>Amazon SES</b>.</p>
    </body>
    </html>"""
    
    CHARSET = "UTF-8"
    
    # Cria cliente SES
    client = boto3.client('ses', region_name=AWS_REGION)
    
    try:
        # Envia o e-mail
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
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Erro ao enviar email: {e.response['Error']['Message']}")
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(f"Email enviado! Message ID: {response['MessageId']}")
        }
