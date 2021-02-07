#import image related items
import picamera
import os
from PIL import Image, ImageDraw, ImageOps

#import GPIO related items set GPIO24(pin18) as output
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

from google.cloud import vision
client = vision.ImageAnnotatorClient()
image_name = 'image.jpg'
#image_distracted = 'distracted.jpg'

def takephoto():
    global camera 
    camera = picamera.PiCamera()
    camera.capture(image_name)

def draw_face_rectangle(image_in, rect_in):
    im = Image.open(image_in)
    f,e = os.path.splitext(image_in)
    image_out = f + "_out_boundrectangle" + e
    print("image out is named: "+ image_out)

    draw = ImageDraw.ImageDraw(im)
    draw.rectangle(rect_in)
    im.save(image_out)


def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    with open(image_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # print(faces)

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
    #print('Faces:')

    #landmark
    landmark_type = ('RIGHT_EYE')
    landmark_type2=('LEFT_EYE')
    print('EYES: ')
    a = 0;
    

    for face in faces:
        #print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        #print('LEFTEYE: {}'.format(landmark_type[face.Landmark.Type.LEFT_EYE_PUPIL]))
        print('LEFTEYE: {}'.format(landmark_type2[face.Landmark.Type.LEFT_EYE]))
        print('RIGHTEYE: {}'.format(landmark_type[face.Landmark.Type.RIGHT_EYE]))
        #print('LEFTPUPIL: {}'.format(landmark_type[face.Landmark.Type.LEFT_PUPIL]))

        a = face.Landmark.Type.LEFT_EYE
        #print(a)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        rectangle = []
        rectangle.append((face.bounding_poly.vertices[0].x,face.bounding_poly.vertices[0].y))
        rectangle.append((face.bounding_poly.vertices[2].x,face.bounding_poly.vertices[2].y))
        print('face bounds: {}'.format(','.join(vertices)))

        draw_face_rectangle(image_name, rectangle)

#When eyes were not detected
    if a == 0:
          filenamecaptured = "image.jpg"
          imgPIL = Image.open(filenamecaptured)
          newimgPIL = imgPIL.resize((400,400))
          newimgPIL.show()
          GPIO.output(24,1)
          sleep(1)
          GPIO.output(24,0)
          #GPIO.cleanup()
#When eyes were not detected
    else:
      #GPIO.cleanup()
      #show image
      filenamecaptured = "image_out_boundrectangle.jpg"
      imgPIL = Image.open(filenamecaptured)
      newimgPIL = imgPIL.resize((400,400))
      newimgPIL.show()

    camera.close()

if __name__ == '__main__':

    main()

