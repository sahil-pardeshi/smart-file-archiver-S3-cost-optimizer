import boto3
import os

s3 = boto3.client('s3')
ses = boto3.client('ses')

BUCKET = 'smart-file-archiver-v3'
EMAIL = 'sahilpardeshi205@gmail.com'

def lambda_handler(event, context):
    result = s3.list_objects_v2(Bucket=BUCKET)
    counts = {"deleted_empty": 0, "deleted_corrupted": 0, "archived": 0}
    
    log_messages = []  # Collect for email body
    
    for obj in result.get('Contents', []):
        key = obj['Key']
        try:
            head = s3.head_object(Bucket=BUCKET, Key=key)
            size = head['ContentLength']
            
            if size == 0:
                s3.delete_object(Bucket=BUCKET, Key=key)
                print(f"Deleted EMPTY file: {key}")
                log_messages.append(f"Deleted EMPTY file: {key}")
                counts['deleted_empty'] += 1
                continue
            
            # Basic check for corruption (by extension)
            if not key.lower().endswith(('.txt', '.pdf', '.jpg')):
                s3.delete_object(Bucket=BUCKET, Key=key)
                print(f"Deleted CORRUPTED/UNSUPPORTED file: {key}")
                log_messages.append(f"Deleted CORRUPTED/UNSUPPORTED file: {key}")
                counts['deleted_corrupted'] += 1
                continue

            # Determine retention
            if key.endswith('.txt'):
                access_days = 30
            else:
                access_days = 60

            # Apply tag
            s3.put_object_tagging(
                Bucket=BUCKET,
                Key=key,
                Tagging={
                    'TagSet': [
                        {'Key': 'RetentionDays', 'Value': str(access_days)}
                    ]
                }
            )
            print(f"Tagged for ARCHIVING: {key} → RetentionDays={access_days}")
            log_messages.append(f"Tagged for ARCHIVING: {key} → RetentionDays={access_days}")
            counts['archived'] += 1

        except Exception as e:
            error_msg = f"Error processing {key}: {str(e)}"
            print(error_msg)
            log_messages.append(error_msg)

    # Build email body
    body = f"""Smart File Archiver v2 Report:

🗂️ Summary:
✅ Empty files deleted: {counts['deleted_empty']}
❌ Corrupted files deleted: {counts['deleted_corrupted']}
📦 Files marked for archiving: {counts['archived']}

📄 File Actions:
""" + "\n".join(log_messages)

    print("📨 Sending summary email...")
    print(body)

    # Send email
    ses.send_email(
        Source='sahilpardeshi205@gmail.com',
        Destination={'ToAddresses': ['sahilpardeshi205@gmail.com']},
        Message={
            'Subject': {'Data': 'Smart File Archiver v2 Report'},
            'Body': {'Text': {'Data': body}}
        }
    )

    return {
        'status': 'Success',
        'summary': counts,
        'details': log_messages
    }

