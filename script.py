import mdl
from display import *
from matrix import *
from draw import *
import math

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    systems = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    polygons = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    for i in p[0]:
        print i
        if i[0] == 'sphere':
            #print 'SPHERE\t' + str(args)
            add_sphere(polygons,
                       float(i[1]), float(i[2]), float(i[3]),
                       float(i[4]), step_3d)
            matrix_mult( systems[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []

        elif i[0] == 'torus':
            #print 'TORUS\t' + str(args)
            add_torus(polygons,
                      float(i[1]), float(i[2]), float(i[3]),
                      float(i[4]), float(i[5]), step_3d)
            matrix_mult( systems[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []

        elif i[0] == 'box':
            #print 'BOX\t' + str(args)
            add_box(polygons,
                    float(i[1]), float(i[2]), float(i[3]),
                    float(i[4]), float(i[5]), float(i[6]))
            matrix_mult( systems[-1], polygons )
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            polygons = []

        elif i[0] == 'circle':
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(i[1]), float(i[2]), float(i[3]),
                       float(i[4]), step)
            matrix_mult( systems[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif i[0] == 'hermite' or i[0] == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(i[1]), float(i[2]),
                      float(i[3]), float(i[4]),
                      float(i[5]), float(i[6]),
                      float(i[7]), float(i[8]),
                      step, i[0])
            matrix_mult( systems[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif i[0] == 'line':
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(i[1]), float(i[2]), float(i[3]),
                      float(i[4]), float(i[5]), float(i[6]) )
            matrix_mult( systems[-1], edges )
            draw_lines(eges, screen, zbuffer, color)
            edges = []

        elif i[0] == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(i[1]), float(i[2]), float(i[3]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif i[0] == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(i[1]), float(i[2]), float(i[3]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif i[0] == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(i[2]) * (math.pi / 180)
            if i[1] == 'x':
                t = make_rotX(theta)
            elif i[1] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif i[0] == 'push':
            systems.append( [x[:] for x in systems[-1]] )

        elif i[0] == 'pop':
            systems.pop()

        elif i[0] == 'display' or i[0] == 'save':
            if i[0] == 'display':
                display(screen)
            else:
                save_extension(screen, i[1] + i[2])
