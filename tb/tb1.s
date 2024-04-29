                # BENCH 1 #
#
#    Explication : Benchmark élementaire/naif
#
#    Registre (durant tout le test)
#    t0 = 5
#    t1 = 10
#
#    On ne test pas ici les suptilités de chaque instruction (TEST NAIF!!)
#    1 : ADD, SUB, XOR, OR, AND, SLL, SRL, SRA, SLT, SLTU
#    2 : ADDI, XORI, ORI, ANDI, SLLI, SRLI, SRAI, SLTI, SLTIUM
#    3 : LB, LH, LBU, LHU
#    4 : SB, SH, SW
#    5 : BEQ, BNE, BLT, BGE, BLTU, BGEU
#

# Affectation des registres t0 et t1 #
    addi t0, t0, 0x5
    addi t1, t1, 0xA

# 1 #

    # ADD
    add x1, t0, t1
    sw x1, 0(x0)        # MEM(0)=15=OxF

    # SUB
    sub x1, t1, t0
    sw x1, 4(x0)        # MEM(1)=5=Ox5

    # XOR
    xor x1, t0, t1      # 0b1001 ^ 0b10010 = 0b11011
    sw x1, 8(x0)        # MEM(2) = 15 = 0xF

    # OR
    or x1, t0, t1       # 0b1001 | 0b10010 = 0b11011
    sw x1, 12(x0)       # MEM(3) = 15 = 0xF

    # AND
    and x1, t0, t1      # 1001 & 10010 = 0
    sw x1, 16(x0)       # MEM(4) = 0 = 0x0

    # SLL
    sll x1, t0, t1      # 5 << 10 
    sw x1, 20(x0)       # MEM(5) = 5120 = 0x1400

    # SRL
    srl x1, t0, t1      # 1001 >> 10 = 0
    sw x1, 24(x0)       # MEM(6) = 0 = 0x0

    # SRA
    sra x1, t0, t1      # 1001 >> 10 = 0
    sw x1, 28(x0)       # MEM(7) = 0 = 0x0

    # SLT
    slt x1, t0, t1      # (1001 < 10)?1:0 = 1
    sw x1, 32(x0)       # MEM(8) = 1 = 0x1

    # SLTU
    sltu x1, t0, t1     # (1001 < 10)?1:0 = 1
    sw x1, 36(x0)       # MEM(9) = 1 = 0x1

# 2 #

    # ADDI
    addi x1, x0, 5     
    sw x1, 40(x0)       # MEM(10) = 5 = 0x5

    # XORI
    xori x1, t0, 0xF    
    sw x1, 44(x0)       # MEM(11) = 10 = 0xa

    # ORI
    ori x1, t0, 0xF   
    sw x1, 48(x0)       # MEM(12) = 15 = 0xF 

    # ANDI
    andi x1, t0, 0xF    
    sw x1, 52(x0)       # MEM(13) = 5 = 0x5 
    
    # SLLI
    slli x1, t0, 0x1   
    sw x1, 56(x0)       # MEM(14) = 10 = 0xA 

    # SRLI
    srli x1, t0, 0x1   
    sw x1, 60(x0)       # MEM(15) = 2 = 0x2 

    # SRAI
    srai x1, t0, 0x1  
    sw x1, 64(x0)       # MEM(16) = 2 = 0x2 

    # SLTI
    slti x1, t0, -1  
    sw x1, 68(x0)       # MEM(17) = 0 = 0x0 

    # SLTIU
    sltiu x1, t0, -1  
    sw x1, 72(x0)       # MEM(18) = 1 = 0x1

# 3 #

    # LB
    lb x1, 0(x0)
    sw x1, 76(x0)       # MEM(19) = 15 =0xf

    # LH
    lh x1, 0(x0)
    sw x1, 80(x0)       # MEM(20) = 15 =0xf

    # LW
    lw x1, 0(x0)
    sw x1, 84(x0)       # MEM(21) = 15 =0xf

    # LBU
    lbu x1, 0(x0)
    sw x1, 88(x0)       # MEM(22) = 15 = 0Xf

    # LHU
    lhu x1, 0(x0)
    sw x1, 92(x0)       # MEM(23) = 15 = 0xf

# 4 #

    # SW
    sw t0, 96(x0)       # MEM(24) = 5 = 0x5

    # SB
    sb t0, 100(x0)      # MEM(25) = 5 = 0x5

    # SH
    sh t0, 104(x0)      # MEM(26) = 5 = 0x5


# 5 #

# MEM(24..30) = 5 = 0x5

beq_test:
    beq t0, t0, beq_test_valid
    j bne_test

bne_test:
    bne t0, t1, bne_test_valid
    j blt_test

blt_test:
    blt t0, t1, blt_test_valid
    j bge_test

bge_test:
    bge t1, t0, bge_test_valid
    j bltu_test

bltu_test:
    bltu t0, t1, bltu_test_valid
    j bgeu_test

bgeu_test:
    bgeu t1, t0, bgeu_test_valid
    j end

beq_test_valid:
    sw t0, 108(x0)
    j bne_test

bne_test_valid:
    sw t0, 112(x0)
    j blt_test

blt_test_valid:
    sw t0, 116(x0)
    j bge_test

bge_test_valid:
    sw t0, 120(x0)
    j bltu_test

bltu_test_valid:
    sw t0, 124(x0)
    j bgeu_test

bgeu_test_valid:
    sw t0, 128(x0)
    j end


end:
    j end# fin bouclé
