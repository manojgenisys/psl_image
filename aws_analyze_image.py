#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-custom-labels-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
from flask import Blueprint,request, jsonify, abort
import json
import base64                    
import requests


web = Blueprint('web', __name__,url_prefix="/psl")



def display_image(bucket,photo,response,img_byte):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    # stream = io.BytesIO(s3_response['Body'].read())
    stream = io.BytesIO(img_byte)
    image=Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('/arial/arial.ttf', 50)
            draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    image.show()

def show_custom_labels(model,bucket,photo, min_confidence,img_byte):
    client=boto3.client('rekognition')

    ###  Call DetectCustomLabels using image path of the bucket
    # response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
    #     MinConfidence=min_confidence,
    #     ProjectVersionArn=model)

    #############

    ######## call this method with image byte, no need to pass bucket path ###


    response = client.detect_custom_labels(
        Image={
            'Bytes': img_byte
        },
         ProjectVersionArn=model,
         MinConfidence=min_confidence
    )    

    # For object detection use case, uncomment below code to display image.
    display_image(bucket,photo,response,img_byte)
    # print(response)
    # return len(response['CustomLabels'])
    return response

    


@web.get("/upload")
def upload():
    

    api = 'http://localhost:5000/psl/compare'
    image_file = 'White Pills Missing.jpeg'
    image_file2 = 'White Pills Missing.jpeg'
    with open(image_file, "rb") as f:
        im_bytes = f.read()        
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    with open(image_file2, "rb") as f2:
        im_bytes2 = f2.read()        
    im_b64_2 = base64.b64encode(im_bytes2).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    payload = json.dumps({"image": im_b64, "image2": im_b64_2})
    response = requests.post(api, data=payload, headers=headers)
    data = ''
    try:
        data = response.json()     
        print(data)                
    except requests.exceptions.RequestException:
        print(response.text)
    return data

@web.post("/compare")
def compare():
    
    ### taking image input from mobile app ####
     # print(request.json)      
    if not request.json or 'image' not in request.json: 
        abort(400)             
    # get the base64 encoded string
    im_b64_1 = request.json['image']
    im_b64_2 = request.json['image2']
    # convert it into bytes  
    img_bytes1 = base64.b64decode(im_b64_1.encode('utf-8'))
    img_bytes2 = base64.b64decode(im_b64_2.encode('utf-8'))
    # convert bytes data to PIL Image object
    # img = Image.open(io.BytesIO(img_bytes))
    image_byte_array1 = io.BytesIO(img_bytes1).getvalue()
    image_byte_array2 = io.BytesIO(img_bytes2).getvalue()
    # img.show()
    ### end of mobile app retrival and process ##

    bucket='custom-labels-console-us-east-1-a92d9baccf'
    photo = 'testing_psl/a2.jpg'
    # photo = 'testing_psl/source_yellow.jpeg'
    model='arn:aws:rekognition:us-east-1:043406298667:project/psl_img2/version/psl_img2.2023-05-18T14.11.16/1684399277799'
    min_confidence=40

    # psl_img3
    # photo = 'psl_img3/Data_Combined/Neozep/00000005.jpg'
    # # photo = 'testing_psl/Neozep.png'
    # photo = 'testing_psl/neozep2.png'
    # model='arn:aws:rekognition:us-east-1:043406298667:project/psl_img3/version/psl_img3.2023-05-25T09.40.45/1684987840656'
    # min_confidence=30

    # label_count=show_custom_labels(model,bucket,photo, min_confidence)
    res1 =  show_custom_labels(model,bucket,photo, min_confidence,image_byte_array1)
    res2 = show_custom_labels(model,bucket,photo, min_confidence,image_byte_array2)
    # print(f'result 2:{res2}')
    len1 = len(res1['CustomLabels'])
    # print(str(len1))
    len2 = len(res2['CustomLabels'])
    b=False
    if len1==len2:
       b=True
    else:
       b = False 

    resJson =  '{ "Image1objects":'+str(len1)+', "Image2objects":'+str(len2)+', "isMatch":"'+str(b)+'"}'
    y = json.loads(resJson)
    print(y)
    return y



########

def show_custom_labels2(model,bucket,photo, min_confidence,img_byte=0):
    client=boto3.client('rekognition')

    ###  Call DetectCustomLabels using image path of the bucket
    # response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
    #     MinConfidence=min_confidence,
    #     ProjectVersionArn=model)

    #############

    ######## call this method with image byte, no need to pass bucket path ###


    response = client.detect_custom_labels(
        Image={
            'Bytes': img_byte
        },
        ProjectVersionArn=model,
         MinConfidence=min_confidence
    )    

    # For object detection use case, uncomment below code to display image.
    display_image(bucket,photo,response,img_byte)
    # print(response)
    # return len(response['CustomLabels'])
    return response


@web.post("/compare2")
def compare2():
    
    ### taking image input from mobile app ####
     # print(request.json)      
    # if not request.json or 'image' not in request.json: 
    #     abort(400)             
    # # get the base64 encoded string
    # im_b64 = request.json['image']
    # # convert it into bytes  
    # img_bytes = base64.b64decode(im_b64.encode('utf-8'))
    # # convert bytes data to PIL Image object
    # img = Image.open(io.BytesIO(img_bytes))
    # # img.show()
    ### end of mobile app retrival and process ##

    bucket='custom-labels-console-us-east-1-a92d9baccf'
    photo = 'testing_psl/a2.jpg'
    # photo = 'testing_psl/source_yellow.jpeg'
    model='arn:aws:rekognition:us-east-1:043406298667:project/psl_img2/version/psl_img2.2023-05-18T14.11.16/1684399277799'
    min_confidence=40


    # with Image.open('White Pills Missing.jpeg') as image:
    #     # Convert the image to bytes
    #     image_byte_array = io.BytesIO()
    #     image.save(image_byte_array, format='JPEG')
    #     image_bytes = image_byte_array.getvalue()
    
    image_file = 'White Pills Missing.jpeg'
    with open(image_file, "rb") as f:
        im_bytes = f.read()        
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    res1 =  show_custom_labels2(model,bucket,photo, min_confidence,image_bytes)
    print(res1)
    return res1

# if __name__ == "__main__":
#     compare2()