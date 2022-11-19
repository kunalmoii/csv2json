import os
from google.cloud import storage
import json
storage_client = storage.Client.from_service_account_json("./credentials/gcp_key.json")

def download_blob(message):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    bucket_name = "input-bucket-2e42ed"

    # The ID of your GCS object
    source_blob_name = str(message)

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    gcp_file_name_split = message.split('/')
    image_name = gcp_file_name_split[-1]
    blob = bucket.blob(image_name)

    blob.download_to_filename("datasets/moiiai_custom/" + str(image_name))

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, image_name
        )
    )
    
def main():
    json_to_load = 'datasets/moiiai_custom/data.json'
    json_file_load = json.load(open(json_to_load,'r'))
    for key, value in json_file_load.items():
        if key=='images':
            for image in value:
                gcp_file_name = image['file_name']
                download_blob(gcp_file_name)
    
    
if __name__ == '__main__':
    main()
    
    
    