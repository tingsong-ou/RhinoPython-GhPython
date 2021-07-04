import rhinoscriptsyntax as rs
from random import randint

def generateMatrix(xNum, yNum, zNum, showTag=False, showPt=False):
    ptDict = {}
    for z in range(zNum):
        for y in range(yNum):
            for x in range(xNum):
                ptDict[(x, y, z)] = (x*10, y*5, z*10)
    if showPt:
        rs.AddPoints(list(ptDict.values()))
    if showTag:
        for key in ptDict:
            rs.AddTextDot(key, ptDict[key])
    return ptDict

def drawPolyline(ptDict, y=1):
    polylines = []
    xMax = max([key[0] for key in ptDict])
    zMax = max([key[2] for key in ptDict])
    for z in range(zMax):
        for x in range(xMax):
            ptA = ptDict[(x, y, z)]
            ptB = ptDict[(x+1, y, z)]
            ptC = ptDict[(x+1, y, z+1)]
            ptD = ptDict[(x, y, z+1)]
            polylines.append(rs.AddPolyline([ptA, ptB, ptC, ptD, ptA]))
    return polylines

def subDiv(poly, showPt=False, showTag=False):
    srf = rs.AddPlanarSrf(poly)
    rs.RebuildSurface(srf, (3, 3), (4, 4))
    pts = rs.SurfaceEditPoints(srf)
    newPtsDict = {}
    x=0
    for i in range(len(pts)):
        if i>0 and i%4 == 0:
            x+=1
        newPtsDict[(x, i%4)] = pts[i]

    x= randint(0, 2)
    y= randint(0, 2)
    xStep = randint(1, 2)
    yStep = randint(1, 2)
    if x == 2: xStep=1
    if y == 2: yStep=1

    ptA = newPtsDict[(x, y)]
    ptB = newPtsDict[(x+xStep), y]
    ptC = newPtsDict[(x+xStep), (y+yStep)]
    ptD = newPtsDict[x, (y+yStep)]
    newPoly = rs.AddPolyline([ptA, ptB, ptC, ptD, ptA])
    rs.DeleteObjects([poly, srf])

    if showPt:
        rs.AddPoints(pts)
    if showTag:
        for key in newPtsDict:
            rs.AddTextDot(key, newPtsDict[key])

    return newPoly

def solid(fPoly, bPoly):
    fPolyO = rs.OffsetCurve(fPoly, rs.CurveAreaCentroid(fPoly)[0], 0.2, (0, 1, 0))
    bPolyO = rs.OffsetCurve(bPoly, rs.CurveAreaCentroid(bPoly)[0], 0.2, (0, 1, 0))
    srf1 = rs.AddLoftSrf([fPoly, fPolyO])
    srf2 = rs.AddLoftSrf([fPoly,bPoly])
    srf3 = rs.AddLoftSrf([fPolyO,bPolyO])
    srf4 = rs.AddLoftSrf([bPoly,bPolyO])
    obj = rs.JoinSurfaces([srf1, srf2, srf3, srf4], True)
    return obj

def main():
    xNum = 8
    yNum = 2
    zNum = 6

    ptDict = generateMatrix(xNum, yNum, zNum, False)
    backPoly = drawPolyline(ptDict)
    frontPoly = drawPolyline(ptDict, 0)

    for i in range(len(frontPoly)):
        frontPoly[i] = subDiv(frontPoly[i])
        solid(frontPoly[i], backPoly[i])

    rs.Command("_SelCrv")
    rs.Command("_Delete")    

rs.EnableRedraw(False)
rs.Command("_SelAll")
rs.Command("_Delete")
main()
rs.EnableRedraw(True)