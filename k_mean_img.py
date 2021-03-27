import cv2
import sys
import random
import math
import numpy as np

#get image path
imgPath = sys.argv[1]
img = cv2.imread(imgPath)
height, width, channels = img.shape

#get k from input
k = 10
if len(sys.argv) > 2:
    k = int(sys.argv[2])

max_loop = 10
if len(sys.argv) > 3:
    max_loop = int(sys.argv[3])

center = []             #value of center of k cluster (with read green blue)
cluster = []            #posision of point
redCluster = []         #red value of that point
greenCluster = []       #green value of that point
blueCluster = []        #blue value of that point

#list image to save and show different of cluster over the time
listImg = []

#initialze k prototypes
random.seed(1)

while True:
    x = random.randint(0, height - 1)
    y = random.randint(0, width - 1)

    #get color of the randomed point
    newCluster = [img[x,y][0], img[x,y][1], img[x,y][2]]

    #ensure that color is not in list yet
    isNew = True

    for c in center:
        if c == newCluster:
            isNew = False
            break
    
    if isNew:
        center.append(newCluster)

        blueCluster.append([newCluster[0]])
        greenCluster.append([newCluster[1]])
        redCluster.append([newCluster[2]])

        cluster.append([[x, y]])

    if (len(center) == k):
        break

#divide all point into cluster
index = 0       #var to count loop

while True:
    for x in range(0, height):
        for y in range(0, width):
            curColor = [img[x, y][0], img[x, y][1], img[x, y][2]]

            #find cluster by calculate the euclid distance and find the shortest one
            minDistance = 255 * 3
            pos = 0

            for i in range(0, len(center) - 1):
                #get color in the center of the cluster
                c = center[i]       

                #calculate euclid distance
                bdistance = int(curColor[0] - c[0])
                gdistance = int(curColor[1] - c[1])
                rdistance = int(curColor[2] - c[2])
                distance =  math.sqrt(rdistance * rdistance + gdistance * gdistance + bdistance * bdistance)
                
                if distance < minDistance:
                    minDistance = distance
                    pos = i
            
            #add the current point to the nearest cluster
            cluster[pos].append([x, y])

            blueCluster[pos].append(curColor[0])
            greenCluster[pos].append(curColor[1])
            redCluster[pos].append(curColor[2])

    #recenter
    for i in range(0, k):
        center[i][0] = int(np.mean(blueCluster[i]))
        center[i][1] = int(np.mean(greenCluster[i])) 
        center[i][2] = int(np.mean(redCluster[i])) 

        #clear the x y cluster
        cluster[i].clear()

    #save image at any step to see the difference
    img2 = img.copy()
    for i in range (0, k):
        for j in range (0, len(cluster[i])):
            x = cluster[i][j][0]
            y = cluster[i][j][1]
            img2[x][y] = [center[i][0], center[i][1], center[i][2]]
    listImg.append(img2)

    print("Done "+str(index))

    index+=1

    if (index == max_loop):
        break;


#display image
cv2.imshow("Display", img)
i = 0

for img2 in listImg:
    cv2.imshow("Output" + str(i), img2)
    i+=1

while True:
    quitKey = cv2.waitKey(1)

    if quitKey == ord("q"):
        break;

cv2.destroyAllWindows()