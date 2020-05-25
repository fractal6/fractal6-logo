#!/usr/bin/python3

"""fractal generation.

Usage:
  fractal.py [-t T] [-k K] [-c C] [-e E] [--theta O] [--space S] [--rayon R] [--exp EXP] [--write]

Options:
  -h --help         Show this screen.
  -t T              Number of point to generate [default: 10].
  -k K              Scaling factor [default: 10].
  -e E              Spiral exponent [default: 2.718].
  -o, --theta O     Angle, multiple of PI [default: 2].
  -s, --space S     Space time [default: lin].
  -c, --category C  piral category [default: quad].
  -r, --rayon R     Rayon factor for svg [default: 1].
  --exp N     Rayon factor for svg [default: 1].
  -w, --write       Write to svg file

Examples:
 ./fractal.py -t 10 -k 2 -e 1.666 -s log -r 1
 ./fractal.py -t 18 -k 4 -s log -o 4.1 -c log -r 1 -w
 ./fractal.py -t 19 -k 4 -s log -o 4.3 -c log --rayon 1.2 --exp 0.9 -w
 ./fractal.py -t 9 -k 3.3 -s log -o 3.2 -c log --rayon 20 --exp 0.6 -w
 ./fractal.py -t 42 -k 4 -s log -o 4.05 -c log --rayon 1 --exp 0.9 -w # fractal2
 ./fractal.py -t 75 -k 5 -s log -o 4.05 -c log --rayon 1 --exp 0.9 -w # fractal3
 ./fractal.py -t 50 -k 5 -s log -o 4.05 -c log --rayon 1.2 --exp 0.95 -w # fractal4

"""

import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt


class Spiral:

    def logspiral(self, T=10, k=10, e=np.e, theta=2*np.pi, space='lin'):
        if space == 'lin':
            t = np.linspace(0, theta, T)
        elif space == 'log':
            _x = np.arange(T)
            t = (theta+np.e)/np.log(T+np.e) * np.log(_x+np.e) - np.e
        else:
            NotImplementedError

        x = np.cos(t) * e**(t/k - 10)
        y = np.sin(t) * e**(t/k - 10)
        return t, x, y

    def quadspiral(self, T=10, k=10, theta=2*np.pi, space='lin', **kwargs):
        if space == 'lin':
            t = np.linspace(0, theta, T)
        elif space == 'log':
            _x = np.arange(T)
            t = (theta+np.e)/np.log(T+np.e) * np.log(_x+np.e) - np.e
        else:
            NotImplementedError

        x = np.cos(t) * t**k
        y = np.sin(t) * t**k
        return t, x, y


def generate_circles_html(tt, xx, yy, r=1, exp=1):

    circles = []
    for t, x, y in zip(tt, xx, yy):
        circle = '<circle cx="{x}" cy="{y}" r="{r}"/>'.format(x=x, y=y, r=(t*r)**exp)
        circles.append(circle)

    circles = "\n".join(circles)
    return circles


def generate_circles_elm(tt, xx, yy, r=1, exp=1):

    circles = []
    for t, x, y in zip(tt, xx, yy):
        circle = 'circle [cx "{x}", cy "{y}", r "{r}"] []'.format(x=x, y=y, r=(t*r)**exp)
        circles.append(circle)

    circles = "\n,".join(circles)
    return circles


if __name__ == '__main__':

    args = docopt(__doc__, version='Fractal 0.0')

    T = int(args['-t'])
    K = float(args['-k'])
    e = float(args['-e'])
    theta = float(args['--theta']) * np.pi
    space = args['--space']
    exp = float(args['--exp'])

    rayon = float(args['--rayon'])

    spiralfun = getattr(Spiral(), args['--category']+"spiral")

    t, x, y = spiralfun(T=T, k=K, e=e, theta=theta, space=space)

    # Translate
    x1 = x - 2*(x - x[0]) + 0.000125
    y1 = y - 2*(y - y[0]) - 0.0001

    minX = np.min([x.min(), x1.min()])
    minY = np.min([y.min(), y1.min()])

    padding = np.abs(x[2]-x[1])

    # Redress negativ value
    if minX < 0:
        x += - minX + padding
        x1 += - minX + padding
    if minY < 0:
        y += - minY + padding
        y1 += - minY + padding

    scale = 1
    if x.max() < 200:
        scale = 200 / x.max()

    # Scale
    x *= scale
    y *= scale

    x1 *= scale
    y1 *= scale

    # Compute Border
    minX = np.min([x.min(), x1.min()])
    minY = np.min([y.min(), y1.min()])
    maxR = (t.max()*rayon)**exp
    x -= minX - maxR*0.995
    x1 -= minX - maxR*0.995
    y -= minY - maxR*0.995
    y1 -= minY - maxR*0.995

    circles_html = generate_circles_html(t, x, y, r=rayon, exp=exp)
    circles2_html = generate_circles_html(t, x1, y1, r=rayon, exp=exp)
    circles_elm = generate_circles_elm(t, x, y, r=rayon, exp=exp)
    circles2_elm = generate_circles_elm(t, x1, y1, r=rayon, exp=exp)

    maxX = (np.max([x.max(), x1.max()]) + maxR)*1.005
    maxY = (np.max([y.max(), y1.max()]) + maxR)*1.005

    #<circle cx="{CX}" cy="{CY}" r="{R}" fill="#333" style="stroke:white;stroke-width:3" />
    svg_html = """<?xml version="1.0" standalone="no"?>
		<svg xmlns="http://www.w3.org/2000/svg" viewPort="0 0 {maxX} {maxY}" fill="#fff">
        <rect x="0" y="0" width="{maxX}" height="{maxY}" fill="#333" />
		{circles}
		{circles2}
		</svg>""".format(circles=circles_html, circles2=circles2_html,
                   maxX=maxX, maxY=maxY,
                   CX=maxX/2, CY=maxY/2, R=0.99*maxX/2
                  )

    svg_elm = """
        svg [viewBox "0 0 {maxX} {maxY}"
        , height "32"
        , width "64"
        , fill "white"
        ]
        [
		{circles}
		,{circles2}
        ]""".format(circles=circles_elm, circles2=circles2_elm,
                    maxX=maxX, maxY=maxY)

    if args['--write']:
        fn = "fractal.svg"
        print("writing %s" % fn)
        with open(fn, 'w') as _f:
            _f.write(svg_html)

        fn = "fractal.elm"
        with open(fn, 'w') as _f:
            _f.write(svg_elm)
    else:
        plt.scatter(x, y)
        plt.scatter(x1, y1)
        plt.show()
