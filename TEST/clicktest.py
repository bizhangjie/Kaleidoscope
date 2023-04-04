import MyUtils
import math

def generate_points(n,r ,x0=0, y0=0):
    points = []
    n*=2
    for i in range(n):
        theta = 2 * math.pi * i / n
        x = x0 + r * math.cos(theta)
        y = y0 + r * math.sin(theta)
        points.append((x, y))
    return points
def generate_X(step=100):
    line1 = [(x, x * 1080 // 1920) for x in range(1, 1921, step)]
    line2 = [(x, 1080*((1920-x)//1920)) for x in range(1920, 0, -step)]
    points = line1 + line2
    return points


MyUtils.releasescreenlock()

# for point in generate_points(20, 300, 960,540):
for point in generate_X():
    MyUtils.click(point[0], point[1],gap=0)

