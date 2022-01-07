import Rhino.Geometry as rg
import Rhino.Collections as rc
from random import randint, uniform, seed
import ghpythonlib.treehelpers as th

seed(rSeed)

#------------HELPER FUNCTIONS-------

#Step 1: generating pts and handles
def getPtNHandle(curve, startT, handleScale, reversed = False):
    ptPara = curve.NormalizedLengthParameter(startT)[1]
    pt = curve.PointAt(ptPara)
    vec = curve.TangentAt(ptPara)
    vec.Unitize()

    span = curve.Domain[1] - curve.Domain[0]
    interv = rg.Interval(ptPara, ptPara + handleScale)

    if interv[1] > curve.Domain[1]:
        interv = rg.Interval(ptPara - handleScale, ptPara)

    scale = curve.GetLength(interv)
    vec *= scale

    if reversed: vec *= -1
    handle = pt + vec
    return pt, handle


#Step 2: generating Bezier curve
def genBezierCrv(ptA, ptB, handleA, handleB):
    pts = rc.Point3dList([ptA, handleA, handleB, ptB])
    bzCrv = rg.BezierCurve(pts)
    bzCrv = bzCrv.ToNurbsCurve()
    return bzCrv

#Step 3: creating leaf
def genLeaf(curveA, curveB, aPara, bPara, aFac, bFac):
    crvs = []
    count = randint(3, 4)
    for i in range(count):
        minFac = uniform(aFac, aFac + 0.5)
        maxFac = uniform(bFac, bFac + 0.5)
        scales = [minFac, maxFac]

        if i == 1:
            scales[0], scales[1] = scales[1], scales[0]
        if i >= 2:
            midFac = (minFac + maxFac) / 2
            scales[0] = uniform(midFac - 1.5, midFac + 1.5)
            scales[1] = uniform(midFac - 1.5, midFac + 1.5)

        ptA, handleA = getPtNHandle(curveA, aPara, scales[0])
        ptB, handleB = getPtNHandle(curveB, bPara, scales[1], True)

        crv = genBezierCrv(ptA, ptB, handleA, handleB)
        crvs.append(crv)
    return crvs


#---------------PROGRAM-------------------

step = int(step * 100)
aParas = [i/100 for i in range(0, 80, step)]
bParas = [i/100 for i in range(20, 100, step)]

leaves = []

for i in range(1, len(curves), 2):
    currCrv = curves[i]
    leftCrv = curves[i-1]

    try:
        rightCrv = curves[i+1]
    except:
        rightCrv = None

    for j in range(len(aParas)):
        aPara = aParas[j]
        bPara = bParas[j]
        leftLeaves = genLeaf(currCrv, leftCrv, aPara, bPara, aFac, bFac)
        leaves.append(leftLeaves)
        if rightCrv:
            rightLeaves = genLeaf(currCrv, rightCrv, aPara, bPara, aFac, bFac)
            leaves.append(rightLeaves)

a = th.list_to_tree(leaves)
