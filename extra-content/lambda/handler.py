import boto3
import time
import os

def redshift_unload_partitioned(cluster_id, sql_query, s3_path, role, partition_by_column, client = None):
    # Create the Boto3 client
    client = client or boto3.client('redshift-data')
    # Launch the SQL query with Redshift Data API
    execution_id = client.execute_statement(
        ClusterIdentifier=cluster_id,
        Database='dev',
        DbUser='awsuser',
        Sql=f"unload ('{sql_query}') TO '{s3_path}' iam_role '{role}' partition by ({partition_by_column}) csv header parallel off;",
    )['Id']

    # Wait for completion
    status = client.describe_statement(Id=execution_id)['Status']
    print(status)
    while status not in ['FINISHED', 'FAILED']:
        time.sleep(15)
        status = client.describe_statement(Id=execution_id)['Status']
        print(status)
        if status == 'FAILED':
            print(client.describe_statement(Id=execution_id)['Error'])
            return False
        else:
            return True
        
def lambda_handler(event, context):
    # Read the values from the event - event is the dict 'inputs' of the LambdaStep
    cluster_id = event['CLUSTER_ID']
    sql_query = event['SQL_QUERY']
    s3_path = event['S3_PATH']
    role = event['REDSHIFT_ROLE']
    partition_by_column = event['PARTITION_BY_COLUMN']
    # Launch the unload by partition
    status = redshift_unload_partitioned(sql_query, s3_path, role, partition_by_column)
    return {
        'status': status,
        's3_path': s3_path
    }

if __name__=='__main__':
    # Set-up the path and roles
    bucket = 'YOUR_BUCKET_HERE'
    key_prefix = 'some/s3/prefix/where/to/store/data'
    role = 'YOUR_ROLE_ARN_HERE'
    cluster_id = 'YOUR_CLUSTER_ID_HERE'
    sql_query = 'SELECT * from my_table'
    partition_by_column = 'YOUR_COLUMN_TO_PARTITION_BY'
 
    # Define the s3 path
    s3_path = f's3://{bucket}/{key_prefix}/'
    
    # Launch the unload by partition
    status = redshift_unload_partitioned(cluster_id, sql_query, s3_path, role, partition_by_column)
    print(status)
