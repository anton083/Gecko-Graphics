import Gecko.gecko as gecko

g = gecko.Gecko()

for n in range(100):
    g.forward(1)
    gecko.update()
