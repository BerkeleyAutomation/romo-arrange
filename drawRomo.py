import matplotlib
import matplotlib.pyplot as plt


#landing zone looks like:  (x, y, width, height, color)
#object looks like: (x, y, width, height, color)
#romo_info looks like: (x, y, width, height, color, rotation angle in degrees)
def draw_field(figure, axis, landing_zones, romo_info, field_width, field_height, objects):
    axis.yaxis.grid(color='black', linestyle='dashed')
    axis.xaxis.grid(color='black', linestyle='dashed')
    for x in landing_zones:
        rect = matplotlib.patches.Rectangle((x[0], x[1]-x[3]), x[2], x[3], color=x[4])
        circ = matplotlib.patches.Circle((x[0] + x[2]/2.0, x[1]-x[3]/2.0), radius = min(x[2]/4.0, x[3]/4.0), color='black')
        axis.add_patch(rect)
        axis.add_patch(circ)
    for o in objects:
        rect = matplotlib.patches.Rectangle((o[0], o[1]-o[3]), o[2], o[3], color=o[4])
        axis.add_patch(rect)
    romo_rect = matplotlib.patches.Rectangle((romo_info[0], romo_info[1]-romo_info[3]), romo_info[2], romo_info[3], color=romo_info[4])
    romo_stripe = matplotlib.patches.Rectangle((romo_info[0], romo_info[1]-romo_info[3]+2*romo_info[3]/5.0), romo_info[2], romo_info[3]/5.0, color='black')
    romo_stripe2 = matplotlib.patches.Rectangle((romo_info[0]+2*romo_info[2]/5.0, romo_info[1]-romo_info[3]), romo_info[2]/5.0, romo_info[3], color='black')
    #trans = matplotlib.transforms.Affine2D().rotate_deg(romo_info[5])
    #romo_rect.set_transform(trans)
    #romo_stripe.set_transform(trans)
    #romo_stripe2.set_transform(trans)
    #trans = matplotlib.transforms.Affine2D().rotate_deg_around(romo_info[0], romo_info[1]-romo_info[3], romo_info[5])
    #romo_rect.set_transform(trans)
    #print axis.transData
    trans = matplotlib.transforms.Affine2D().rotate_deg_around(romo_info[0], romo_info[1]-romo_info[3], romo_info[5]) + axis.transData
    romo_rect.set_transform(trans)
    romo_stripe.set_transform(trans)
    romo_stripe2.set_transform(trans)
    axis.add_patch(romo_rect)
    axis.add_patch(romo_stripe2)
    axis.add_patch(romo_stripe)
    plt.xlim([0, field_width])
    plt.ylim([0, field_height])
    plt.show()


def main():
    figure = plt.figure()
    axis = figure.add_subplot(111)
    
    landing_zones = [(0, 80, 10, 10, 'pink'), (70, 80, 10, 10, 'yellow'),
                     (70, 10, 10, 10, 'red'), (0, 10, 10, 10, 'green')]
    objects = [(24, 10, 8, 9, 'red'), (60, 70, 6, 6, 'yellow'),
               (30, 20, 5, 5, 'pink'), (60, 50, 3, 3, 'green')]
    rotation = 98
    romo_info = (60, 20, 8, 12, 'gray', rotation)
    field_width = 80
    field_height = 80
    draw_field(figure, axis, landing_zones, romo_info, field_width, field_height, objects)




if __name__ == "__main__":
    main()
