import imageio
import urllib.request
import cv2

url = "https://i.stack.imgur.com/lui1A.gif"
fname = "tmp.gif"

## Read the gif from the web, save to the disk
imdata = urllib.request.urlopen(url).read()
imbytes = bytearray(imdata)
open(fname,"wb+").write(imdata)

## Read the gif from disk to `RGB`s using `imageio.miread` 
gif = imageio.mimread(fname)
nums = len(gif)
print("Total {} frames in the gif!".format(nums))

# convert form RGB to BGR 
imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]

## Display the gif
i = 0

while True:
    cv2.imshow("gif", imgs[i])
    if cv2.waitKey(100)&0xFF == 27:
        break
    i = (i+1)%nums
cv2.destroyAllWindows()