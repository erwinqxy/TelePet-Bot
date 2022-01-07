import cv2
import numpy as np
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Sticker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
# Load the cascade
face_cascade = cv2.CascadeClassifier('computer_vision/haarcascade_frontalface_default.xml')

# Read the input image
#img = cv2.imread('petpet/faces.jpg')
#img = cv2.imread('petpet/test1.jpg')

def face_detect(img):
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Documentation: https://realpython.com/face-recognition-with-python/
    # https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
    # Pre-trained weights: https://github.com/opencv/opencv/tree/master/data/haarcascades
    # Detect faces # detection algorithm uses a moving window to detect objects
    faces = face_cascade.detectMultiScale(gray, 
                                            scaleFactor=1.1, # Since some faces may be closer to the camera, they would appear bigger than the faces in the back. The scale factor compensates for this.
                                            minNeighbors=4 #minNeighbors defines how many objects are detected near the current one before it declares the face found
                                            #minSize=(30, 30), #minSize, meanwhile, gives the size of each window.
                                            )
    # Draw rectangle around the faces
    #for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the output
    #cv2.imshow('img', img)
    # write image
    #cv2.imwrite('petpet/inference-img2.jpg',img)
    #cv2.waitKey()
    return img, faces


def overlay_transparent(background, overlay, x, y, face_w, face_h):

    #height,width = image.shape
    #print(image.shape)
    #width = image.shape[1]#480
    #height= image.shape[0]#640

    # height and width of background image
    background_width = background.shape[1]
    background_height = background.shape[0]

    overlay= cv2.resize(overlay, (face_w, face_h))
    
    # if coordinate x and y is larger than background width and height, stop code
    if x >= background_width or y >= background_height:
        #print(x, y, face_w, face_h)
        return background
    
    # height and width of overlay image
    h, w = overlay.shape[0], overlay.shape[1]

    #print('x:',x)
    #print('overlay_width:',w)
    #print('background_width:',background_width)
    

    #print('y:',y)
    #print('overlay_height:',h)
    #print('background_height:',background_width)
    

    if w >= background_width:
        print(x, y, face_w, face_h)
        return background
    if h >= background_height:
        print(x, y, face_w, face_h)
        return background
    
    # if coordinate x + width of overlay is larger than background width and height, stop code
    if x + w > background_width:
        #w = background_width - x
        #overlay = overlay[:, :w]
        #print(x, y, face_w, face_h)
        return background
    
    # if 
    #if x - w < 2:
        #w = background_width - x
        #overlay = overlay[:, :w]
        #print(x, y, face_w, face_h)
        #return background

    if y + h > background_height:
        #h = background_height - y
        #overlay = overlay[:h]
        #print(x, y, face_w, face_h)
        return background
    
    #if y - h < 2:
        #h = background_height - y
        #overlay = overlay[:h]
        #print(x, y, face_w, face_h)
        #return background
    
    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

#processed_img, predictions = face_detect(img)

#overlay= cv2.imread('petpet/trump-face.png', cv2.IMREAD_UNCHANGED)

#for (x, y, face_w, face_h) in predictions:
    #processed_img = overlay_transparent(processed_img, overlay, x,y,face_w, face_h)

#cv2.imshow('processed img', processed_img)
#cv2.imwrite('petpet/trump-faces.jpg',img)
#cv2.waitKey()

from PIL import Image
#import requests
#import wget
import os
import urllib.request

# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image

#overlay_filename = 'overlay_temp.jpg' #petpet/cv-images/trump-face.png'

overlay_status = 'OFF'

def face_handler(update, context):
    global overlay_status
    #print('face_handler overlay_status:',overlay_status)
    # update image overlay
    group_id = update["message"]["chat"]["id"]
    #print()
    #print(update.message)

    if overlay_status == 'change_overlay':


        if len(update.message.photo) == 0:
            #print('sticker')
            file = update.message.sticker.file_id
        else:
            file = update.message.photo[-1].file_id

        #file = update.message.photo[-1].file_id
        obj = context.bot.get_file(file)
        image_url = obj['file_path']
        np_image = url_to_image(image_url)
        cv2.imwrite(f'computer_vision/cv-images/{group_id}_overlay_temp.jpg',np_image)

        update.message.reply_text("Okay, I have updated your overlay image, you can start replacing faces on images!")
        overlay_status = 'ON'

    # replace face with overlay image
    elif overlay_status == 'ON':
        update.message.reply_text("Give me a sec to make some magic...")
        #if 'sticker' in update['message'].keys():
        #print(len(update.message.photo))
        if len(update.message.photo) == 0:
            #print('sticker')
            file = update.message.sticker.file_id
        else:
            file = update.message.photo[-1].file_id
            
        obj = context.bot.get_file(file)
        #obj.download()
        #print(obj)
        image_url = obj['file_path']
        #im = Image.open(requests.get(url, stream=True).raw)
        #image_url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
        #filename = wget.download(image_url)
        #np_image = cv2.imread(filename)
        np_image = url_to_image(image_url)

        # run face detection
        processed_img, predictions = face_detect(np_image)
        
        # checks which overlay to use
        if os.path.exists(f'computer_vision/cv-images/{group_id}_overlay_temp.jpg'):
            overlay_filename = f'computer_vision/cv-images/{group_id}_overlay_temp.jpg'
        else:
            overlay_filename = 'computer_vision/cv-images/trump-face.png'

        # reads overlay image to np array    
        overlay= cv2.imread(overlay_filename, cv2.IMREAD_UNCHANGED)
        
        # superimpose overlay images onto background image
        for (x, y, face_w, face_h) in predictions:
            processed_img = overlay_transparent(processed_img, overlay, x,y,face_w, face_h)
        
        # save processed image 
        cv2.imwrite(f'computer_vision/cv-images/{group_id}_temp.jpg',processed_img)

        if len(predictions) == 0:
            update.message.reply_text("Hmmm, I cannot seem to find any faces in your image.")
        else:   
            context.bot.send_photo(group_id,photo=open(f'computer_vision/cv-images/{group_id}_temp.jpg', "rb"))
            update.message.reply_text(f"Here you go! I have detected and replaced {len(predictions)} faces!")
        # remove processed image
        os.remove(f'computer_vision/cv-images/{group_id}_temp.jpg')

    # overlay status is OFF
    else:
        pass

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def replace_face_command(update, context):
    
    group_id = update["message"]["chat"]["id"]
    #print(update)
    #print('\n')
    #print(context.args)
    #context.bot.send_photo(group_id, open("petpet/inference-img2.jpg", "rb"))
    #print('update_overlay_command overlay_status:',overlay_status)
    
    #print(update.message)

    list_of_buttons = ['Replace Face ON', 'Replace Face OFF','Change Face Overlay']
    button_list = []
    for each in list_of_buttons:
        button_list.append(InlineKeyboardButton(each, callback_data = each))

    #reply_markup = InlineKeyboardMarkup(button_list)
    reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) #n_cols = 1 is for single column and mutliple rows
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

    #update.message.reply_text(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)

def button(update, context):
    global overlay_status

    
    query = update.callback_query
    group_id = update.callback_query.message.chat.id
    #query.answer()
    
    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data
    #print(context)
    
    # Now u can define what choice ("callback_data") do what like this:
    if choice == 'Replace Face ON':
        #func1()
        context.bot.send_message(group_id,"Let's start replacing faces, please send me an image!")
        #print('option 1')
        overlay_status = 'ON'

    if choice == 'Replace Face OFF':
        #func2()
        context.bot.send_message(group_id,"Replace face function turned off")
        #print('option 2')
        overlay_status = 'OFF'

    if choice == 'Change Face Overlay':
        #update.message.reply_text("Please send me an image to replace the face overlay (use .png for best results)")
        #print('option 3')
        context.bot.send_message(group_id,"Please send me an image to replace the face overlay (use .png for best results)")
        #update.send_message(group_id, text='option 3')
        overlay_status = 'change_overlay'

'''
def sticker_handler(update, context):
    global overlay_status
    #print('face_handler overlay_status:',overlay_status)
    # update image overlay
    group_id = update["message"]["chat"]["id"]
    #print(update.message)
    file = update.message.sticker.file_id

    obj = context.bot.get_file(file)
    #print(obj)
    image_url = obj['file_path']
    np_image = url_to_image(image_url)
    #cv2.imwrite(f'{group_id}_sticker.jpg',np_image)

    # run face detection
    processed_img, predictions = face_detect(np_image)
    
    # checks which overlay to use
    if os.path.exists(f'computer_vision/cv-images/{group_id}_overlay_temp.jpg'):
        overlay_filename = f'computer_vision/cv-images/{group_id}_overlay_temp.jpg'
    else:
        overlay_filename = 'computer_vision/cv-images/trump-face.png'

    # reads overlay image to np array    
    overlay= cv2.imread(overlay_filename, cv2.IMREAD_UNCHANGED)
    
    # superimpose overlay images onto background image
    for (x, y, face_w, face_h) in predictions:
        processed_img = overlay_transparent(processed_img, overlay, x,y,face_w, face_h)
    
    # save processed image 
    cv2.imwrite(f'computer_vision/cv-images/{group_id}_temp.jpg',processed_img)

    if len(predictions) == 0:
        update.message.reply_text("Hmmm, I cannot seem to find any faces in your image.")
    else:   
        context.bot.send_photo(group_id,photo=open(f'computer_vision/cv-images/{group_id}_temp.jpg', "rb"))
        update.message.reply_text(f"Here you go! I have detected and replaced {len(predictions)} faces!")
    # remove processed image
    os.remove(f'computer_vision/cv-images/{group_id}_temp.jpg')
    

    #https://stackoverflow.com/questions/34355648/telegram-getting-file-id-for-existing-sticker
'''