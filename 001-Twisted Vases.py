import rhinoscriptsyntax as rs
from random import random

def generateMatrix(xMax, yMax, zMax, showPoints = False):
    ptMatrix = {}
    for z in range(zMax):
        for y in range(yMax):
            for x in range(xMax):
                ptMatrix[(x, y, z)] = (x * 8, y * 8, z * 8)
    
    if showPoints:
        rs.AddPoints(list(ptMatrix.values()))
    return ptMatrix

def generateCrvs(matrix, xMax, yMax, zMax):
    crvDict = {}
    for i in range(yMax):
        crvDict[i] = []
    
    for y in range(yMax):
        for x in range(xMax-1):
            for z in range(zMax-1):
                ptA = matrix[(x, y, z)]
                ptB = matrix[(x+1, y, z)]
                ptC = matrix[(x+1, y, z+1)]
                ptD = matrix[(x, y, z+1)]
                pts = [ptA, ptB, ptC, ptD, ptA]
                crv = rs.AddCurve(pts)
                scaleCrv(crv)
                crvDict[y].append(crv)
    
    return crvDict

def loftCrv(crvDict, yMax):
    result = []
    for i in range(len(crvDict[0])):
        crvs = [crvDict[y][i] for y in range(yMax)]
        result.append(rs.AddLoftSrf(crvs))
    return result

def scaleCrv(crv, max=1.1, min=0.5):
    cen = rs.CurveAreaCentroid(crv)[0]
    xFactor = random() * (max - min) + min
    zFactor = random() * (max - min) + min
    rs.ScaleObject(crv, cen, (xFactor, 1, zFactor))

xMax = 8
yMax = 3
zMax = 6

ptMatrix = generateMatrix(xMax, yMax, zMax)
crvDict = generateCrvs(ptMatrix, xMax, yMax, zMax)
srf = loftCrv(crvDict, yMax)