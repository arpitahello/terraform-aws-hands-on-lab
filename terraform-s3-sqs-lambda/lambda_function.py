import json
import urllib.parse

def lambda_handler(event, context):

    print("===== EVENT RECEIVED =====")

    for record in event.get("Records", []):

        try:
            # SQS body (string) → JSON
            body = json.loads(record.get("body", "{}"))

            # Ensure it's a valid S3 event structure
            if "Records" not in body:
                print("Skipping non-S3 message:", body)
                continue

            for s3_record in body["Records"]:

                bucket = s3_record["s3"]["bucket"]["name"]
                
                # Decode S3 object key (handles spaces and special characters)
                key = urllib.parse.unquote_plus(
                    s3_record["s3"]["object"]["key"]
                )

                print("Bucket:", bucket)
                print("File Name:", key)

        except Exception as e:
            print("Error processing record:", str(e))
            continue

    return {
        "statusCode": 200
    }