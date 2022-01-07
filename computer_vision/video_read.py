import cv2
import numpy as np


import cv2

background = cv2.imread("computer_vision/cv-images/trump-face.png", cv2.IMREAD_UNCHANGED)
foreground = cv2.imread("computer_vision/cv-images/trump-face.png", cv2.IMREAD_UNCHANGED)

# normalize alpha channels from 0-255 to 0-1
alpha_background = background[:,:,3] / 255.0
alpha_foreground = foreground[:,:,3] / 255.0

# set adjusted colors
for color in range(0, 3):
    background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
        alpha_background * background[:,:,color] * (1 - alpha_foreground)

# set adjusted alpha and denormalize back to 0-255
background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

# display the image
cv2.imshow("Composited image", background)
cv2.waitKey(0)

'''
video_url = 'https://api.telegram.org/file/bot5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc/videos/file_123.mp4'
#video_url = 'https://www.learningcontainer.com/download/sample-mp4-video-file-download-for-testing/'

video_url = 'https://api.telegram.org/file/bot5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc/animations/file_127.mp4'
video_url = 'https://api.telegram.org/file/bot5007007064:AAETfWXVt6Z4ilnW7-Rlltz43NmScS1JTAc/animations/file_129.mp4'
#import urllib.request
#urllib.request.urlretrieve(video_url, 'video_name.mp4') 

#capture = cv2.VideoCapture(video_url)
#if not vcap.isOpened():
#    print "File Cannot be Opened"
video = cv2.VideoCapture(video_url)

width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = video.get(cv2.CAP_PROP_FPS)

fourcc = 0x7634706d
videoWriter = cv2.VideoWriter(f'_video_temp.mp4', fourcc, fps, (int(width), int(height)))

while(True):
    # Capture frame-by-frame
    ret, frame = video.read()
    # print cap.isOpened(), ret
    if frame is not None:
        # Display the resulting frame
        #frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('frame',frame)
        # Press q to close the video windows before it ends if you want
        videoWriter.write(frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        print("Frame is None")
        break

# When everything done, release the capture
#capture.release()
video.release()
videoWriter.release()
cv2.destroyAllWindows()
'''