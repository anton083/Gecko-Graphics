
from gecko import Gecko, update

g = Gecko()

for n in range(100):
    g.forward(1)
    update()
