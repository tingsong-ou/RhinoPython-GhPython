import rhinoscriptsyntax as rs
from random import random

def divCrv(crv, vNum, dir):
    pts = []
    crvLen = rs.CurveLength(crv)
    lenStep = float(crvLen / (vNum)) #I can remove * 2 later
    if dir == 0:
        pts = rs.DivideCurveLength(crv, lenStep / 3)
    else:
        tempPts = rs.DivideCurveLength(crv, lenStep / 6)
        newStart = rs.CurveClosestPoint(crv, tempPts[1])
        newEnd = rs.CurveClosestPoint(crv, tempPts[-2])
        crv = rs.TrimCurve(crv, [newStart, newEnd], False)
        pts = rs.DivideCurveLength(crv, lenStep / 3)

    endPt = rs.CurveEndPoint(crv)
    if pts[-1] != endPt:
        pts.append(endPt)
    return pts


def addCrvs(srf, ptDict, uNum, i, offStart, offEnd):
    crvs = []
    for j in range(offStart, offEnd, 1):
        pts = []
        for k in range(uNum + 1):
            if k % 2 == 0:
                pts.append(ptDict[k][i])
            else:
                pts.append(ptDict[k][i + j])
        crvs.append(rs.AddInterpCurve(pts))
    return crvs


def drawEdges(ptDict, uNum, srf):
    crvs = []
    for i in range(len(ptDict[0])):
        if i % 3 == 0 and i != 0 and i != len(ptDict[0]) - 1:
            crvs += addCrvs(srf, ptDict, uNum, i, -2, 2)
            '''
            for j in range(-2, 2, 1):
                pts = []
                for k in range(uNum + 1):
                    if k % 2 == 0:
                        pts.append(ptDict[k][i])
                    else:
                        pts.append(ptDict[k][i + j])
                crvs.append(rs.AddInterpCurve(srf,pts))
            '''
        elif i == 0:
            crvs += addCrvs(srf, ptDict, uNum, i, 0, 2)
        elif i == len(ptDict[0]) - 1:
            crvs += addCrvs(srf, ptDict, uNum, i, -2, 0)
        else:
            pts = []
            for k in range(uNum+1):
                if k % 2 == 0:
                    pts.append(ptDict[k][i])
                else:
                    pts.append(ptDict[k][i - (i % 3 - 1)])
            crvs.append(rs.AddInterpCurve(pts))
    return crvs


def divSrf(srf, uNum, vNum, srfOffset):
    crvs = []
    ptDict = {}
    uDom = rs.SurfaceDomain(srf, 0)
    vDom = rs.SurfaceDomain(srf, 1)

    uStep = (uDom[1] - uDom[0]) / uNum

    for i in range(uNum + 1):
        baseCrv = rs.ExtractIsoCurve(srf, (uDom[0] + i * uStep, 0), 1)[0]
        pts = divCrv(baseCrv, vNum, i % 2)
        for j in range(len(pts)):
            if (j + i % 2 * 2) % 3 != 0:
                norm = rs.BrepClosestPoint(srf, pts[j])[3]
                norm = rs.VectorUnitize(norm)
                if i == 0 or i == uNum: norm = (norm[0], norm[1], 0)
                norm = rs.VectorScale(norm, srfOffset * (0.2 + random() * 1.2))
                rs.MoveObject(pts[j], norm)
        ptDict[i] = pts
    crvs += drawEdges(ptDict, uNum, srf)

    return crvs


#Main
srfs = []
uNum = int(uNum)
vNum = int(vNum)
if vNum < 2: vNum = 2
if uNum < 4: uNum = 4
if vNum % 2 != 0: vNum += 1

crvs = divSrf(srf, uNum, vNum, offDist)

for i in range(len(crvs) - 1):
    srfs += rs.AddLoftSrf([crvs[i], crvs[i+1]])

if rs.IsSurfaceClosed(srf, 1):
    srfs += rs.AddLoftSrf([crvs[0], crvs[-1]])