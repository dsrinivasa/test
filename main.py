import base64
from google.cloud import asset_v1
def export_tasks(request):
    # create client
    client = asset_v1.AssetServiceClient()
    #print("""This Function was triggered by messageId {} published at {} to {}
    #""".format(context.event_id, context.timestamp, context.resource["name"]))
    # bq partition spec
    # PARTITION_KEY_UNSPECIFIED = 0
    # READ_TIME = 1
    # REQUEST_TIME = 2
    partition_spec = asset_v1.PartitionSpec()
    partition_spec.partition_key = 1
    # init request
    output_config = asset_v1.OutputConfig()
    output_config.bigquery_destination.dataset = "projects/second-flame-351109/datasets/cloud_assets"
    output_config.bigquery_destination.table = "data"
    output_config.bigquery_destination.force = True
    output_config.bigquery_destination.parition_spec = partition_spec
    request = asset_v1.ExportAssetsRequest(
        parent = "projects/second-flame-351109",
        content_type = "RESOURCE",
        asset_types = [
            "cloudfunctions.googleapis.com/CloudFunction",             
            "compute.googleapis.com/ForwardingRule",
            "iam.googleapis.com.*",
            "logging.googleapis.com/LogBucket"
        ],
        output_config = output_config,
    )
    # make request
    operation = client.export_assets(request=request)
    
    msg_body = base64.b64decode(event['data']).decode('utf-8')
    print('Exporting: {}'.format(msg_body))
    response = operation.result()
    # handle response
    print(response)
