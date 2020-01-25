import boto3
import twitter

CONSUMER_KEY_PARAM_NAME = '/{}/consumer_key'.format('tsgt_green')
CONSUMER_SECRET_PARAM_NAME = '/{}/consumer_secret'.format('tsgt_green')
ACCESS_TOKEN_PARAM_NAME = '/{}/access_token'.format('tsgt_green')
ACCESS_TOKEN_SECRET_PARAM_NAME = '/{}/access_token_secret'.format('tsgt_green')

SSM = boto3.client('ssm')

param_names=[
    CONSUMER_KEY_PARAM_NAME,
    CONSUMER_SECRET_PARAM_NAME,
    ACCESS_TOKEN_PARAM_NAME,
    ACCESS_TOKEN_SECRET_PARAM_NAME
]

response = SSM.get_parameters(
    Names=param_names,
    WithDecryption=True
)

#print(response)

param_lookup = {param['Name']: param['Value'] for param in response['Parameters']}
print(param_lookup)
api = twitter.api(
    consumer_key=param_lookup[CONSUMER_KEY_PARAM_NAME],
    consumer_secret=param_lookup[CONSUMER_SECRET_PARAM_NAME],
    access_token_key=param_lookup[ACCESS_TOKEN_PARAM_NAME],
    access_token_secret=param_lookup[ACCESS_TOKEN_SECRET_PARAM_NAME]
)


# status = 'Test from Lambda #python'
# post_update = api.PostUpdate(status=status)