import Rhino.Geometry as rg
import random
import ghpythonlib.treehelpers as th
from math import *

random.seed(seed)

#Generating Pentagon
def genPenta(line):
    iter = 0
    oriPts = [line.From, line.To]
    pentaPts = [line.To]
    while iter < 3:
        vec = rg.Point3d.Subtract(line.To, line.From)
        rad = radians(72);
        nextX = vec[0] * cos(rad) - vec[1] * sin(rad);
        nextY = vec[0] * sin(rad) + vec[1] * cos(rad);
        newPt = rg.Point3d(nextX, nextY, 0)
        newPt += line.To
        newLine = rg.Line(line.To, newPt)
        line = newLine
        pentaPts.append(line.To)
        iter += 1
    pentaPts.append(oriPts[0])
    return pentaPts


#Adding Edge to avaliable edge set
def addEdges(pentaPts, edgeSet):
    for i in range(len(pentaPts)):
        ptA = pentaPts[i]
        ptB = pentaPts[(i+1)%len(pentaPts)]
        newEdge = rg.Line(ptA, ptB)
        edgeSet.add(newEdge)


#Moving pts
def movePts(pentaPts):
    newPts = pentaPts[:]
    for i in range(1, len(pentaPts)-1):
        pt = pentaPts[i]
        xOff = random.uniform(-0.7, 0.7)
        yOff = random.uniform(-0.7, 0.7)
        zOff = random.uniform(-1.0, 3.0)
        newPts[i] = rg.Point3d(pt[0] + xOff, pt[1] + yOff, pt[2] + zOff)
    return newPts
        

#Check intersection
def checkIntersection(pentagonA, pentagonB):
    pPentaA = [rg.Point3d(pt[0], pt[1], 0) for pt in pentagonA]
    pPentaB = [rg.Point3d(pt[0], pt[1], 0) for pt in pentagonB]
    
    #Shorten PolylineA
    tempA = rg.PolylineCurve(pPentaA)
    dom = tempA.Domain
    tempA = tempA.Trim(dom[0] + 0.1, dom[1] - 0.1)
    pPentaA[0] = tempA.PointAtStart
    pPentaA[-1] = tempA.PointAtEnd
    
    #Create Closed Polygons
    polyA = rg.PolylineCurve(pPentaA + [pPentaA[0]])
    polyB = rg.PolylineCurve(pPentaB + [pPentaB[0]])
    
    plane = rg.Plane.WorldXY
    rel = rg.Curve.PlanarClosedCurveRelationship(polyA, polyB, plane, 0.01)
    
    return rel != rg.RegionContainment.Disjoint
    


avalEdges = {line}
pentagons = []
currItr = 0

while currItr < iter:
    currItr += 1
    randEdge = random.choice(list(avalEdges))
    randEdge.Flip()
    newPenta = genPenta(randEdge)
    newPenta = movePts(newPenta)
    
    #Check Collision
    isCollide = False
    for penta in pentagons:
        intersect = checkIntersection(newPenta, penta)
        if intersect: isCollide = True
    if isCollide: continue
    
    pentagons.append(newPenta)
    addEdges(newPenta, avalEdges)
    avalEdges.remove(randEdge)
    

a = th.list_to_tree(pentagons)