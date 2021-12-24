import Rhino.Geometry as rg
from random import random, uniform, sample, seed, randint
import ghpythonlib.treehelpers as th

seed(1000)

#Step 1: move vertices, making shape dynamic
def moveVertices(polyline):
    ptNum = polyline.PointCount
    pts = []
    planePts = []
    #Getting points and moving vectors
    for i in range(ptNum):
        pts.append(polyline.Point(i))
        if len(planePts) <= 3:
            planePts.append(pts[i])
    plane = rg.Plane(planePts[0], planePts[1], planePts[2])
    dir = plane.ZAxis

    #Update point position
    for i in range(ptNum):
        scalar = uniform(0.0, 2.0)
        vec = dir * scalar
        pts[i] = pts[i] + vec
    pts[-1] = pts[0]

    #Preserving plane for future modifications
    return pts, plane


#Step 2: Cell type A
#Dividing a polygon into three parts: halfA, halfB, curve
def divPolygon(vertices, plane):
    midIdx = len(vertices) // 2
    startPt = vertices[0]
    endPt = vertices[midIdx]

    #get polygon centroid
    centroid = getCentroid(vertices)

    xOff = plane.XAxis * uniform(0.0, 2.0)
    yOff = plane.YAxis * uniform(0.0, 2.0)
    zOff = plane.ZAxis * uniform(1.0, 3.0)

    centroid[0] += xOff[0] + yOff[0] + zOff[0]
    centroid[1] += xOff[1] + yOff[1] + zOff[1]
    centroid[2] += xOff[2] + yOff[2] + zOff[2]

    curve = rg.Curve.CreateInterpolatedCurve([startPt, centroid, endPt], 3)
    curve = jagCurve(curve, plane, 24)
    curve = rg.PolylineCurve(curve)

    halfA = rg.PolylineCurve(vertices[:midIdx+1])
    halfB = rg.PolylineCurve(vertices[midIdx:])
    halfB.Reverse()
    return [curve, halfA, halfB]



#Step 3: Cell type B
def offsetPolygon(vertices, plane):
    centroid = getCentroid(vertices)
    dist = uniform(0.3, 0.4)
    height = uniform(1.0, 2.0)
    newPts = []

    for i in range(len(vertices)):
        v = vertices[i]
        vec = (centroid - v) * dist
        vec += plane.ZAxis * height
        newPts.append(v + vec)

    curve = rg.NurbsCurve.Create(True, 3, newPts[:-1])
    curve = jagCurve(curve, plane, 30, 1)
    curve = rg.PolylineCurve(curve)

    outer = rg.PolylineCurve(vertices)
    inner = rg.Circle(plane, centroid, uniform(0.3, 1))

    #Change curve seam (I can do this at the end)!!!
    startT = curve.ClosestPoint(vertices[0])[1]
    curve.ChangeClosedCurveSeam(startT)

    inner = inner.ToNurbsCurve()
    inStartT = inner.ClosestPoint(vertices[0])[1]
    inner.ChangeClosedCurveSeam(inStartT)


    return [curve, outer, inner]




#Get centroid from a serise of vertices
def getCentroid(vertices):
    centroid = [0, 0, 0]
    for i in range(len(vertices) - 1):
        centroid[0] += vertices[i][0]
        centroid[1] += vertices[i][1]
        centroid[2] += vertices[i][2]
    centroid = [val / (len(vertices) - 1) for val in centroid]
    return rg.Point3d(centroid[0], centroid[1], centroid[2])



#Making a smooth curve jaggy
def jagCurve(curve, plane, divisions, mode = 0):
    totalLen = curve.GetLength()
    lenStep = totalLen / divisions
    #These are parameters

    #This is the c# array pattern
    ts = curve.DivideByLength(lenStep, True)
    ts = [t for t in ts]
    if mode == 1: ts.append(curve.Domain[1])

    offDist = uniform(0.2, 0.5)
    pts = []
    for i in range(len(ts)):
        t = ts[i]
        newPt = curve.PointAt(t)
        if i % 2 != 0 and i != (len(ts)-1):
            if mode == 1: vec = -plane.ZAxis
            else:
                vec = curve.CurvatureAt(t)
                vec.Unitize()
                vec = -plane.ZAxis + vec
            vec = vec * offDist
            newPt = newPt + vec
        pts.append(newPt)
    return pts




##Operations


newCells = []
planes = []
newBases = []

for poly in cells:
    vertices, plane = moveVertices(poly)
    planes.append(plane)
    newBases.append(rg.PolylineCurve(vertices))
    if randint(0, 1) == 0:
        newCells.append(divPolygon(vertices, plane))
    else:
        newCells.append(offsetPolygon(vertices, plane))

newCells = th.list_to_tree(newCells)
