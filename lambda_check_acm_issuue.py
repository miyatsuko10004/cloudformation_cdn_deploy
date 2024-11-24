import json
import boto3
import time

def lambda_handler(event, context):
    acm_client = boto3.client('acm', region_name='us-east-1')
    certificate_arn = event['ResourceProperties']['CertificateArn']
    physical_resource_id = event.get('PhysicalResourceId', certificate_arn)
    timeout = time.time() + 900  # 15分のタイムアウト

    while True:
        response = acm_client.describe_certificate(CertificateArn=certificate_arn)
        status = response['Certificate']['Status']
        if status == 'ISSUED':
            send_response(event, context, "SUCCESS", {}, physical_resource_id)
            break
        elif time.time() > timeout:
            send_response(event, context, "FAILED", {}, physical_resource_id, "Certificate issuance timed out.")
            break
        else:
            time.sleep(30)  # 30秒待機

def send_response(event, context, response_status, response_data, physical_resource_id, reason=None):
    response_url = event['ResponseURL']
    response_body = {
        'Status': response_status,
        'Reason': reason or 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': physical_resource_id,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    }
    json_response_body = json.dumps(response_body)
    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }
    try:
        import urllib3
        http = urllib3.PoolManager()
        response = http.request('PUT', response_url, headers=headers, body=json_response_body)
    except Exception as e:
        print("send_response failed: {}".format(e))
