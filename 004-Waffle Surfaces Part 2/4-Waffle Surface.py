import rhinoscriptsyntax as rs
from math import pi, sin
from random import random, seed

seed(rSeed)

#--------FUNCTIONS--------

#CREATING THE CURVED SURFACE
def createSrf(xNum = 10, yNum = 10, xStep = 5, yStep = 5):
    startAng = 0
    xPeriod = 2 * pi
    yPeriod = 2 * pi
    curves = []
    for y in range(yNum + 1):
        pts = []
        for x in range(xNum + 1):
            xAngStep = xPeriod / xNum
            pts.append((x * xStep, y * yStep, 2 * sin(x * xAngStep + startAng)))
        curves.append(rs.AddCurve(pts))
        startAng += yPeriod / yNum
    return rs.AddLoftSrf(reversed(curves))


#SUBDIVIDING SURFACE
def divideSrf(srf):
    uDomain = rs.SurfaceDomain(srf, 0)
    vDomain = rs.SurfaceDomain(srf, 1)

    uSteps = u #u is a GhPython input
    vSteps = v #v is a GhPython input

    srfPts = {}
    polys = []
    normals = []

    for j in range(len(vSteps)):
        for i in range(len(uSteps)):
            uPos, vPos = uSteps[i], vSteps[j]
            if uPos != 0 and uPos != 1 and vPos != 0 and vPos != 1:
                uPos += random() * 0.04 - 0.02
                vPos += random() * 0.04 - 0.02
            currU = uDomain[0] + uPos * (uDomain[1] - uDomain[0])
            currV = vDomain[0] + vPos * (vDomain[1] - vDomain[0])

            pt = rs.EvaluateSurface(srf, currU, currV)
            srfPts[(i, j, 0)] = pt
            normal = normalPt(srf, [currU, currV], amp)
            normals.append(normal)
            srfPts[(i, j, 1)] = rs.PointAdd(pt, normal)

            if i > 0 and j > 0:
                for n in range(2):
                    ptA = srfPts[(i, j, n)]
                    ptB = srfPts[(i, j-1, n)]
                    ptC = srfPts[(i-1, j-1, n)]
                    ptD = srfPts[(i-1, j, n)]
                    polys.append(rs.AddPolyline([ptA, ptB, ptC, ptD, ptA]))

    return srfPts, polys


#CALCULATING THE SURFACE NORMAL ON SPECIFIC UV POSITION
def normalPt(srf, uv, amplitude):
    normal = rs.SurfaceNormal(srf, uv)
    normal = rs.VectorScale(normal, amplitude * (1 + random() * 0.5))
    return normal


def scalePoly(poly, scale):
    pts = rs.CurveEditPoints(poly)[:-1]
    ptsX = [pt[0] for pt in pts]
    ptsY = [pt[1] for pt in pts]
    ptsZ = [pt[2] for pt in pts]
    ptNum = len(pts)
    avgCen = (sum(ptsX)/ptNum, sum(ptsY)/ptNum, sum(ptsZ)/ptNum)

    outPoly = rs.ScaleObject(poly, avgCen, (scale, scale, scale), True)

    return outPoly

#--------EXECUSION--------

#VISUALIZATION THE RESULT
srf = createSrf(10, 10, xStep, yStep)
srfPts, polys= divideSrf(srf)
srfPts = rs.AddPoints(list(srfPts.values()))

polysA = [polys[i] for i in range(len(polys)) if i % 2 == 0]
polysB = [polys[i] for i in range(len(polys)) if i % 2 == 1]

outSrfs = []

for i in range(len(polysA)):
    newSrfs = []
    polyAO = scalePoly(polysA[i], 0.9)
    polyBO = scalePoly(polysB[i], 0.9)
    newSrfs += rs.AddLoftSrf([polysB[i], polyBO])
    newSrfs += rs.AddLoftSrf([polysA[i], polyAO])
    newSrfs += rs.AddLoftSrf([polysA[i], polysB[i]])
    newSrfs += rs.AddLoftSrf([polyAO, polyBO])
    outSrfs.append(rs.JoinSurfaces(newSrfs))
    
