import rhinoscriptsyntax as rs
from random import random, seed

seed(100)

def offsetPts(ptDict, attrPt, magnitude, srf):
    maxDist = max([rs.Distance(attrPt, pt) for pt in ptDict.values()])
    minDist = min([rs.Distance(attrPt, pt) for pt in ptDict.values()])
    for pt in ptDict.values():
        norm = rs.BrepClosestPoint(srf, pt)[3]
        plane = rs.PlaneFromNormal(pt, norm)
        randVec = (random() - 0.5, random() - 0.5, random() - 0.5)
        newLoc = rs.PointAdd(pt, randVec)
        newLoc = rs.PlaneClosestPoint(plane, newLoc)
        moveVec = rs.VectorSubtract(newLoc, pt)
        moveVec = rs.VectorUnitize(moveVec)

        dist = rs.Distance(attrPt, pt)
        remapDist = int((dist - minDist) / (maxDist - minDist) * 1000) / 1000
        rs.MoveObject(pt, rs.VectorScale(moveVec, remapDist * magnitude))

def drawHexa(ptDict):
    polys = []
    vMax = max([key[0] for key in ptDict])
    uMax = max([key[1] for key in ptDict])
    for v in range(vMax - 1):
        for u in range(v%2, uMax - v % 2, 2):
            pt1 = ptDict[v, u]
            pt2 = ptDict[v, u+1]
            pt3 = ptDict[v+1, u+1]
            pt4 = ptDict[v+2, u+1]
            pt5 = ptDict[v+2, u]
            pt6 = ptDict[v+1, u]
            pts = [pt1, pt2, pt3, pt4, pt5, pt6, pt1]
            polys.append(rs.AddPolyline(pts))
    return polys


def divDom(srf, uNum, vNum):
    pts = {}
    uDom = rs.SurfaceDomain(srf, 0)
    vDom = rs.SurfaceDomain(srf, 1)
    uStep = (uDom[1] - uDom[0]) / uNum
    vStep = (vDom[1] - vDom[0]) / vNum

    for v in range(vNum + 1):
        vParam = vDom[0] + v * vStep
        uIndex = 0
        for u in range(uNum + 1):
            if u % 3 == 1 and v % 2 == 0:
                uParam = uDom[0] + (u - 0.5) * uStep
                pts[v, uIndex] = rs.EvaluateSurface(srf, uParam, vParam)
                uIndex += 1
                uParam = uDom[0] + (u + 0.5) * uStep
                pts[v, uIndex] = rs.EvaluateSurface(srf, uParam, vParam)
                uIndex += 1
            elif u % 3 != 1 and v % 2 == 1:
                uParam = uDom[0] + u * uStep
                pts[v, uIndex] = rs.EvaluateSurface(srf, uParam, vParam)
                uIndex += 1
    return pts




uNum = int(uNum)
vNum = int(vNum)


if uNum < 5: uNum = 5
if uNum > 5 and (uNum - 5) % 3 != 0:
    uNum += 3 - (uNum - 5) % 3

a = divDom(srf, uNum, vNum)
offsetPts(a, attrPt, magnitude, srf)
c = drawHexa(a)

b = a.keys()
a = a.values()

