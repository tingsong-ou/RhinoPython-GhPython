import rhinoscriptsyntax as rs
from math import pi, sin

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


def divideSrf(srf):
    uDomain = rs.SurfaceDomain(srf, 0)
    vDomain = rs.SurfaceDomain(srf, 1)

    uSteps = u
    vSteps = v

    srfPts = {}
    polys = []
    normals = []

    for j in range(len(vSteps)):
        for i in range(len(uSteps)):
            uPos, vPos = uSteps[i], vSteps[j]
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


def normalPt(srf, uv, amplitude):
    normal = rs.SurfaceNormal(srf, uv)
    normal = rs.VectorScale(normal, amplitude)
    return normal


srf = createSrf(10, 10, xStep, yStep)
srfPts, polys= divideSrf(srf)
srfPts = rs.AddPoints(list(srfPts.values()))