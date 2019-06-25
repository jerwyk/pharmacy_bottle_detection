import time 
import requests
import cv2
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline 

def processRequest(url, json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json() ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result

def locateObjectOnImage(result, img, obj='person'):
    detect_result = pd.DataFrame(result['predictions'])
    #detect_result = detect_result[detect_result['object'] == obj]
    
    h, w, c = img.shape
    
    for i in range(len(detect_result)):
        rectangle = detect_result.iloc[i]['boundingBox']
        x1 = int(rectangle['left'] * w)
        y1 = int(rectangle['top'] * h)
        x2 = x1 + int(rectangle['width'] * w)
        y2 = y1 + int(rectangle['height'] * h)
        cv2.rectangle(img,(x1, y1),(x2, y2),(255,0,0),2)
        cv2.putText( img, detect_result.iloc[i]['tagName'], (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3 )

cap = cv2.VideoCapture(0)

count = 0
img_num = 0

#-----------------------------
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Prediction-key': '89144758eb7f4b3dba0fd99271ececd3',
}

p_url = 'https://northcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/6cad7b44-cde9-4fdc-8aaf-d34672e5ac96/detect/iterations/Iteration4/image?%s'

#data = None

# Load raw image file into memory

# Computer Vision parameters
params = None

headers = dict()
headers['Prediction-Key'] = '89144758eb7f4b3dba0fd99271ececd3'
headers['Content-Type'] = 'application/json'

#json = {'url': 'https://www.wonderlabs.com/1200size/5383.jpg'}
json = None

result = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    img = frame

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if(count >= 120):
        count = 0
        cv2.imwrite("frame\\f%d.jpg" % img_num, frame)
        pathToFileInDisk = "frame\\f%d.jpg" % img_num
        with open( pathToFileInDisk, 'rb' ) as f:
            data = f.read()

        result = processRequest(p_url, json, data, headers, params)
        if result is not None:
            # Load the original image, fetched from the URL
            data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
            img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )

    if result is not None:
            # Load the original image, fetched from the URL
            
            locateObjectOnImage(result, img, obj='lines')

        
    cv2.imwrite("frame\\r%d.jpg" % img_num, img)

    # Display the resulting frame
    cv2.imshow('frame', img)

    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()