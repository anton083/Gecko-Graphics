from gecko import Gecko, update

def right_angle(g, direction):
    d = direction
    
    g.set_pencolor(black)
    g.penup()
    g.forward(15)
    g.rotate(d*90)
    g.pendown()
    g.forward(15)
    g.rotate(d*90)
    g.forward(15)
    g.rotate(d*90)
    g.penup()
    g.forward(15)
    g.rotate(d*90)
    g.pendown()

angle_step = 0.02
min_angle = 0
max_angle = 40

# 1 cm = {scale} pixels
scale = 12

red = '#cc0000'
green = '#00cc00'
blue = '#0044cc'
black = '#000000'

dist1 = 14
dist2 = 7
dist3 = 9

g = Gecko()
g.auto_update = False

g.penup()
g.set_position((0,0))
g.pendown()

angle = min_angle
while angle <= max_angle:
    angle += angle_step

    g.set_angle(angle)


    # I split the lines into two parts so I can take a pause
    # and write the text in the middle
    g.set_pencolor(red)
    g.forward(dist1*scale/2)
    g.write(f'{dist1} cm')
    g.forward(dist1*scale/2)
    g.left(90)

    right_angle(g, 1)
    
    g.set_pencolor(green)
    g.forward(dist2*scale/2)
    g.write(f'{dist2} cm')
    g.forward(dist2*scale/2)
    g.right(90)

    right_angle(g, -1)
    
    g.set_pencolor(blue)
    g.forward(dist3*scale/2)
    g.write(f'{dist3} cm')
    g.forward(dist3*scale/2)

    x, y = g.position
    side_length = round((x+y)/2/scale,1)

    g.set_pencolor(black)

    # Draw Rectangle
    g.set_position((x,y/2))
    g.write(f'{side_length} cm')
    g.set_position((x,0))
    g.set_position((0,0))
    g.set_position((0,y))
    g.set_position((x,y))

    update()

    if round(x,1) == round(y,1):
        rounded_angle = round(angle, 2)
        print("Side length found!", side_length, "cm")
        print("The angle should be roughly", rounded_angle)

        colors = [red, green, blue, black]
        g.set_angle(135)
        circumference = 3.14159*x*1.41421
        for n in range(360):

            # I learned about this today.
            # It's apparently very efficient compared to doing a bunch of ifs.
            match n:
                case 120:
                    g.write('hehe')
                case 186:
                    g.write(f'angle = {rounded_angle}')

            g.set_pencolor(colors[n//90])
            g.left(1)
            g.forward(circumference/360)
            update()
        
        break

    g.clear()
    
    g.penup()
    g.set_position((0,0))
    g.pendown()
