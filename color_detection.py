import argparse
import cv2
import pandas as pd
import numpy as np

#Setup argparser to read image file location directly from cmd prompt
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Read image with opencv
img = cv2.imread(img_path)

#Declaring global variables to be used later
clicked = False
r = g = b = xpos = ypos = 0

#Read csv file with pandas library, give name values to each column
index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names = index, header = None)

#Define callback function for a mouse event. Function will calculate the RGB values of the pixel on double click.

def draw_function(event, x, y, flags, param) :
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r, g, b, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[x,y]
        b = int(b)       
        g = int(g)
        r = int(r)
        

#Create window to display image, then call callback function on mouse event
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)



#Define function to return the color name from RGB values. To get the color name, calculate a distance which tells us how close we are to a color and choose the one having minimum distance

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            colorName = csv.loc[i, "color_name"]
    return colorName

#Draw the image one the window. When a double click occurs, draw a rectangle and get the color name to draw text on the window.

while(1):
    cv2.imshow("image",img)
    if (clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        #Creating text string to display ( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
  #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break
cv2.destroyAllWindows()

