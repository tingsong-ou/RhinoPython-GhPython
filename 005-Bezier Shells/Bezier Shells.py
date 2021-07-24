import rhinoscriptsyntax as rs
import Rhino.Geometry as rhg
import Rhino.Collections as rhc
from random import randint, random, seed

seed(rSeed)

def addBezierShell(poly):
    beziers = []
    pts = rs.CurveEditPoints(poly)
    startPt = randint(0, 1)

    for i in range(startPt, len(pts)-1, 2):
        pta = rhg.Point3d(pts[i])
        ptb = rhg.Point3d(pts[i+1])
        span = rs.Distance(pta, ptb) * zFactor
        aHandle = rhg.Point3d(pta[0], pta[1], pta[2] + span + (random() * 2 - 1) * span)
        bHandle = rhg.Point3d(ptb[0], ptb[1], ptb[2] + span + (random() * 2 - 1) * span)
        ptList = rhc.Point3dList(pta, aHandle, bHandle, ptb)
        bezier = rhg.BezierCurve(ptList)
        bezier = bezier.ToNurbsCurve()

        if i == startPt + 2: bezier.Reverse()

        beziers.append(bezier)
    return beziers

shells = []
for poly in polys:
    shells += addBezierShell(poly)




