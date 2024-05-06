                # BENCH CORDIC #
#
#    Explication : Benchmark de l'unité CORDIC
# Virgule fixe, 8-24



li t0, 0x03243f6a # pi
li t1, 0x01921fb5 # pi/2

corcos x1, t0 # cos(pi) = -1
sw x1, 0(x0)

corsin x1, x0 # sin(pi/2) = 1
sw x1, 4(x0)
