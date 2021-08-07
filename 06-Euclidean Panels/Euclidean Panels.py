import rhinoscriptsyntax as rs

def drawRect(xPos, yPos, width, height):
    plane = rs.WorldXYPlane()
    plane = rs.MovePlane(plane, (xPos, yPos, 0))
    rect = rs.AddRectangle(plane, width, height)
    return [rect]

def divSquare(xPos, yPos, width, thrd, ratio):
    rects = []
    itr = 0
    xEndPos = width + xPos
    yEndPos = width + yPos
    rects += drawRect(xPos, yPos, width, width)
    while width > thrd:
        itr += 1
        if itr % 2 == 1:
            while xPos + width * ratio < xEndPos + 0.1:
                rects += divRect(xPos, yPos, width * ratio, thrd, ratio)
                xPos += width * ratio
            width = xEndPos - xPos
        else:
            while yPos + width / ratio < yEndPos + 0.1:
                rects += divRect(xPos, yPos, width, thrd, ratio)
                yPos += width / ratio
            width = yEndPos - yPos
    return rects

def divRect(xPos, yPos, width, thrd, ratio):
    rects = []
    itr = 0
    xEndPos = xPos + width
    yEndPos = yPos + width / ratio
    rects += drawRect(xPos, yPos, width, width/ratio)
    while width > thrd:
        itr += 1
        if itr % 2 == 0:
            while xPos + width < xEndPos + 0.1:
                rects += divSquare(xPos, yPos, width, thrd, ratio)
                xPos += width
            width = xEndPos - xPos
        else:
            while yPos + width < yEndPos + 0.1:
                rects += divSquare(xPos, yPos, width, thrd, ratio)
                yPos += width
            width = yEndPos - yPos
    return rects



numA = x
numB = y
thrd = limit
if thrd < 30: thrd = 30
ratio = float(numA / numB)
if(numA != numB):
    a = divSquare(0, 0, 500, thrd, ratio)