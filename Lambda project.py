import io
import boto3
import json
import os
from PIL import Image
import requests
from io import StringIO
import numpy
import urllib


ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')
def lambda_handler(event, context):
        
        data = json.loads(json.dumps(event))
        # payload = data['body']
        # payload = payload['url']
        # print(payload)
        url = "https://mynovpotatobucket1.s3.us-east-2.amazonaws.com/data1a/defect_free/0002.jpg"

        imgdata = urllib.request.urlopen(urllib.request.Request(
        url=url,
        headers={'Accept': 'application/jpg'},
        method='GET'),
        timeout=10).read()
        
        
        imgdata = io.BytesIO(imgdata)
        
        img = Image.open(imgdata)
       
        img = img.resize((28, 28), Image.ANTIALIAS)
        
        # img = numpy.array(img,dtype=numpy.float32)
        
        # img = numpy.expand_dims(img, axis=0)
        # print("dhhd")
        # f_img=numpy.resize(img,(1,28,28))
        # print(type(f_img))
        # print("are")
        # print(f_img)
        # print("ok")
        
        
        # payload = json.dumps(f_img.tolist())

        # img_data = Image.open(requests.get(url, stream=True).raw).convert('L')
        # aqua = np.array(img_data)
        # aqua = aqua.reshape(28,28,1)
        # aqua = aqua.tolist()
        # data = json.dumps([aqua])
        # payload = data
        
        response = runtime.invoke_endpoint(EndpointName='IC-data1a-1670108238', ContentType='application/x-image', Body=imgdata)

        result = json.loads(response['Body'].read().decode())
        
        # Prepare state data
        detected_class = "defect_free" if result[0] > result[1] else "defective"
        score = result[0] if detected_class == "defect_free" else result[1]
        score = str(score)

        # test = "test"
        # return payload