from minesw import *

f = MinerField(20, 20)

print(" -" * 30)
f.generate_bomb(30)
f.print_field(False)
f.open_tile(2,2)
f.print_field()
print(" -" * 30)
