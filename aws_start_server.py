#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def start_model(project_arn, model_arn, version_name, min_inference_units):
   

    client=boto3.client('rekognition')

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Done...')
    
def main():
    ## for psl_img2
    project_arn='arn:aws:rekognition:us-east-1:043406298667:project/psl_img2/1684391130114'
    model_arn='arn:aws:rekognition:us-east-1:043406298667:project/psl_img2/version/psl_img2.2023-05-18T14.11.16/1684399277799'
    min_inference_units=1 
    version_name='psl_img2.2023-05-18T14.11.16'
    start_model(project_arn, model_arn, version_name, min_inference_units)

    ## for psl_img3
    # # project_arn='arn:aws:rekognition:us-east-1:043406298667:project/psl_img3/1684941349537'
    # # model_arn='arn:aws:rekognition:us-east-1:043406298667:project/psl_img3/version/psl_img3.2023-05-25T09.40.45/1684987840656'
    # # min_inference_units=1 
    # # version_name='psl_img3.2023-05-25T09.40.45'
    # start_model(project_arn, model_arn, version_name, min_inference_units)

# if __name__ == "__main__":
#     main()


## for api
from app import app
@app.route('/')
def index():
    # main()
    return "model is running"
    
if __name__ == "__main__":
    app.run(debug=True,host="127.0.0.1",port=5000)