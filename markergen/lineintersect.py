import numpy as np

 
def check_intersect(p1, q1, p2, q2):
    def on_segment(p, q, r):
        if q[0] > np.max([p[0], r[0]]):
            return False
        if q[0] < np.min([p[0], r[0]]):
            return False
        if q[1] < np.min([p[0], r[0]]):
            return False
        if q[1] > np.max([p[1], r[1]]):
            return False
        if q[1] < np.min([p[1], r[1]]):
            return False
        return True

    def orientation(p, q, r):
        val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
        if val > 0:
            return 'cw'
        elif val < 0:
            return 'ccw'
        else:
            return 'col'

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 'col' and on_segment(p1, p2, q1):
        return True
    if o2 == 'col' and on_segment(p1, q2, q1):
        return True
    if o3 == 'col' and on_segment(p2, p1, q2):
        return True
    if o4 == 'col' and on_segment(p2, q1, q2):
        return True
    return False
