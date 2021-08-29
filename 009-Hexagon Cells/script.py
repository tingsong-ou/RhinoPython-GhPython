import rhinoscriptsyntax as rs
from random import seed, uniform, randint

seed(rSeed)

def getAverageCenter(pts):
    cenX = sum([pts[i][0] for i in range(len(pts) - 1)]) / (len(pts) - 1)
    cenY = sum([pts[i][1] for i in range(len(pts) - 1)]) / (len(pts) - 1)
    cenZ = sum([pts[i][2] for i in range(len(pts) - 1)]) / (len(pts) - 1)
    return (cenX, cenY, cenZ)

#------Pattern A--------
def patternA(hexa, offsetDist):
    crvs = []
    srfs = []
    pts = rs.PolylineVertices(hexa)
    cenPt = getAverageCenter(pts)

    newPts = []
    for i in range(len(pts)):
        moveVec = rs.VectorSubtract(cenPt, pts[i])
        moveVec = rs.VectorUnitize(moveVec)
        moveVec = rs.VectorScale(moveVec, offsetDist)
        newPt = rs.PointAdd(pts[i], moveVec)
        newPts.append(newPt)
    crv = rs.AddCurve(newPts)
    crvs.append(crv)

    #Creating surface
    crvPara = rs.CurveClosestPoint(crv, pts[0])
    crvPt = rs.EvaluateCurve(crv, crvPara)
    secLine = rs.AddLine(pts[0], crvPt)
    srf = rs.AddSweep2([crv, hexa], [secLine])
    srfs += srf

    return crvs, srfs


#------Pattern B--------
def patternB(hexa):
    crvs = []
    srfs = []
    pts = rs.PolylineVertices(hexa)
    cenPt = getAverageCenter(pts)

    for i in range(len(pts) - 1):
        pta = pts[i]
        ptb = pts[i+1]
        ptList = [pta, cenPt, ptb]
        crv = rs.AddCurve(ptList)
        crvs.append(crv)

        #Creating surface
        outline = rs.AddPolyline([pta, cenPt, ptb])
        srf = rs.AddLoftSrf([outline, crv])
        srfs += srf

    return crvs, srfs

#------Pattern C--------
def patternC(hexa):
    crvs = []
    srfs = []
    pts = rs.PolylineVertices(hexa)
    cenPt = getAverageCenter(pts)

    for i in range(len(pts) - 1):
        pta = pts[i]
        ptb = pts[i+1]
        ptList = [pta, cenPt, ptb, pta]
        crv = rs.AddCurve(ptList, 2)
        crvs.append(crv)

        #Creating surface
        outline = rs.AddPolyline(ptList)
        crvPara = rs.CurveClosestPoint(crv, cenPt)
        crvPt = rs.EvaluateCurve(crv, crvPara)
        secLine = rs.AddLine(cenPt, crvPt)
        srf = rs.AddSweep2([outline, crv], [secLine])
        srfs += srf

    return crvs, srfs


#--------Pattern D--------
def patternD(hexa):
    crvs = []
    srfs = []
    pts = rs.PolylineVertices(hexa)
    cenPt = getAverageCenter(pts)

    for i in range(len(pts) - 1):
        pta = pts[i]
        ptb = pts[i+1]
        ptList = [pta, ptb, cenPt, 0]
        subCen = getAverageCenter(ptList)
        segA = rs.AddCurve([pta, subCen, cenPt])
        segB = rs.AddCurve([cenPt, subCen, ptb])
        segC = rs.AddCurve([ptb, subCen, pta])
        crv = rs.JoinCurves([segA, segB, segC])[0]
        crvs.append(crv)

        #Creating surface
        srf = rs.AddEdgeSrf([segA, segB, segC])
        srfs.append(srf)
    return crvs, srfs



#Excuting
crvs = []
srfs = []

for hexa in hexagons:
    pattern = randint(0, 3)
    if pattern == 0:
        offsetDist = uniform(0.8, 2.5)
        crvs += patternA(hexa, offsetDist)[0]
        srfs += patternA(hexa, offsetDist)[1]
    elif pattern == 1:
        crvs += patternB(hexa)[0]
        srfs += patternB(hexa)[1]
    elif pattern == 2:
        crvs += patternC(hexa)[0]
        srfs += patternC(hexa)[1]
    else:
        crvs += patternD(hexa)[0]
        srfs += patternD(hexa)[1]
