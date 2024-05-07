from pynq import MMIO
import numpy as np
import datetime
from time import sleep
import os

class RISCVEIRB_Controller:

    # MMIO REG (32 bits) ADDRESS_OFFSET 
    SLV_REG0_ADDRESS_OFFSET                 = 0x00
    SLV_REG1_ADDRESS_OFFSET                 = 0x04
    SLV_REG2_ADDRESS_OFFSET                 = 0x08
    VAL_MEM_ADDRESS_OFFSET                  = 0x0c
    SIG_ADR_INST_OUT_ADDRESS_OFFSET         = 0x10
    SIG_VAL_OUT_INST_OUT_ADDRESS_OFFSET     = 0x14
    SIG_NEW_ADR_INST_OUT_ADDRESS_OFFSET     = 0x18
    SIG_ADR_MEM_DATA_OUT_ADDRESS_OFFSET     = 0x1c
    SIG_VAL_IN_DATA_OUT_ADDRESS_OFFSET      = 0x20
    SIG_VAL_OUT_DATA_OUT_ADDRESS_OFFSET     = 0x24
    SIG_JALR_ADR_OUT_ADDRESS_OFFSET         = 0x28
    SIG_JR_ADR_OUT_ADDRESS_OFFSET           = 0x2c
    SIG_BR_JAL_ADR_OUT_ADDRESS_OFFSET       = 0x30
    SIG_SEL_FUNC_ALU_OUT_ADDRESS_OFFSET     = 0x34
    SIG_FSM_STATE_OUT_ADDRESS_OFFSET        = 0x38
    SIG_VAL_MEM_DATA_DEPTH_ADDRESS_OFFSET   = 0x3c
    
    def __init__(self, BASE_ADDRESS = 0x43C00000, ADDRESS_LENGTH = 0x64000):
        print("new instance of RISCVEIRB_Controller")
        self.mmio = MMIO(BASE_ADDRESS, ADDRESS_LENGTH)

    ########## METHODES ##########
                
    def slv_reg0_creat(self, CE = 0, Inst_Boot = 0, Data_Boot = 0, Inst_RW_Boot = 0, Data_RW_Boot = 0, Boot = 0, Val_Inst_In_boot = 0, Val_Data_In_Boot = 0):
        # | Port                 | Largeur (bits) | Correspondance                   |
        # | CE                   | 1              | slv_reg0(0)                      |
        # | Inst_Boot            | 1              | slv_reg0(1)                      |
        # | Data_Boot            | 1              | slv_reg0(2)                      |
        # | Inst_RW_Boot         | 1              | slv_reg0(3)                      |
        # | Data_RW_Boot         | 1              | slv_reg0(4)                      |
        # | Boot                 | 1              | slv_reg0(5)                      |
        # | Val_Inst_In_boot     | 8              | slv_reg0(23 downto 16)           |
        # | Val_Data_In_boot     | 8              | slv_reg0(31 downto 24)           |
        if (CE > 1 or Inst_Boot > 1 or Data_Boot > 1 or Inst_RW_Boot > 0 or Data_RW_Boot > 0 or Boot > 0 or Val_Inst_In_boot > 2**8-1 or Val_Data_In_Boot > 2**8-1):
            print("Error : slv_reg0_creat\n")
        slv_reg0 = 0
        slv_reg0 = CE + (Inst_Boot << 1) + (Data_Boot << 2) + (Inst_RW_Boot << 3) + (Data_RW_Boot << 4) + (Boot << 5) + (Val_Inst_In_boot << 16) + (Val_Data_In_Boot << 24)
        print("slv_reg0 :", bin(slv_reg0))
        return slv_reg0
        
    ## WRITE ##

    def write_inst_mem_from_tab(self, mem_instruction, size = 32, print_opt = True):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        CODE_RAM_SIZE = size
        if print_opt:
            print("\nInstruction Memory Write Process\n\r")
        for i in range(0, CODE_RAM_SIZE, 1):
            # Envoie octets par octets
            for j in range (0, 4, 1):
                adresse = (4 * i) + j
                tableauOctets[j]  = (mem_instruction[i] >> (j*8)) % 256
                data_ins = ((0 << 24) + (tableauOctets[j] << 16) + 0b0000000000001010); # Inst_Boot & Inst_RW_Boot
                # Ecriture dans la mémoire octets par octets
                self.mmio.write(0x04, adresse)
                self.mmio.write(0x00, int(data_ins))
            if print_opt:
                print("Octet value Write for current Instruction",hex(mem_instruction[i]),"at address", i,": [",hex(tableauOctets[3]),";",hex(tableauOctets[2]),";",hex(tableauOctets[1]),";",hex(tableauOctets[0]),"]")

    def write_data_mem_from_tab(self, mem_data, size = 32):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        print("\nData Memory Write Process\n\r")
        CODE_RAM_SIZE = size
        for i in range(0, CODE_RAM_SIZE, 1):
            for j in range (0, 4, 1):
                temp = (j  * 8)
                adresse = (4 * i) + j
                tableauOctets[j]  = (mem_data[i]>> temp)%256;
                data_val = (tableauOctets[j] << 24) + ((0 << 16) +  + 0b0000000000010100);
                self.mmio.write(0x08, adresse)    
                self.mmio.write(0x00, data_val)
            print("Octet value Write for current Instruction",hex(mem_data[i]),"at address", i,": [",hex(tableauOctets[3]),";",hex(tableauOctets[2]),";",hex(tableauOctets[1]),";",hex(tableauOctets[0]),"]")
    

    ## READ ##

    def read_inst_mem(self, size = 32, log_opt = True, file_name = "inst_mem", print_opt = True):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        mem_instruction = np.zeros(size)
        CODE_RAM_SIZE = size
        #Instruction Memory Read Process  
        print("\nInstruction Memory Read Process\n\r")
        for i in range(0, CODE_RAM_SIZE, 1):
            for j in range (0, 4, 1):
                self.mmio.write(0x00,0b00000000000000000000000000000010)
                adresse = ((4 * i) + j)
                self.mmio.write(0x04, adresse)
                tableauOctets[j] = self.mmio.read(0xC)>>16
                data_ins_rd = (tableauOctets[3] << 24) + (tableauOctets[2] << 16) + (tableauOctets[1] << 8) + (tableauOctets[0]) 
            mem_instruction[i] = data_ins_rd
            if print_opt:
                print("MEM({}) = {:08X}".format(i, data_ins_rd & 0xFFFFFFFF))  # Fix pour l'affichage sans le moins
         # Enregistrement dans un fichier log    
        if (log_opt):
            now = datetime.datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")  # Ajout de %f pour les microsecondes
            log_file_name = "./log/"+time+"_"+file_name+".hex"
            with open(log_file_name, 'w') as f:
                for value in mem_instruction:
                    fstring = "0x{:08X},\n".format(int(value) & 0xFFFFFFFF)
                    f.write(fstring)
        return mem_instruction

    
    def read_data_mem(self, size = 32, log_opt = True, file_name = "data_mem", print_opt = True):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        mem_data = np.zeros(size)
        CODE_RAM_SIZE = size
        #Data Memory Read Process  
        if print_opt:
            print("\nInstruction Memory Read Process\n\r")
        for i in range(0, CODE_RAM_SIZE, 1):
            for j in range (0, 4, 1):
                # Data_RW_Boot <= 0 (READ)
                # Data_Boot <= 1 
                self.mmio.write(0x00,0b00000000000000000000000000000100)
                adresse = ((4 * i) + j)
                self.mmio.write(0x08, adresse)
                tableauOctets[j] = self.mmio.read(0xC)>>24
    
            data_val_rd = (tableauOctets[3] << 24) + (tableauOctets[2] << 16) + (tableauOctets[1] << 8) + (tableauOctets[0]) 
            # if (data_val_rd  < 0) : 
                # data_val_rd  = (data_val_rd  + (1<<32))
                
            mem_data[i] = data_val_rd
            
            if print_opt:
                print("MEM({}) = {:08X}".format(i, data_val_rd & 0xFFFFFFFF))  # Fix pour l'affichage sans le moins
        # Enregistrement dans un fichier log    
        if (log_opt):
            now = datetime.datetime.now()
            time_extension = now.strftime("%Y-%m-%d_%H-%M-%S-%f")  # Ajout de %f pour les microsecondes
            filename = "./log/"+time_extension+"_"+file_name+".hex"
            with open(filename, 'w') as f:
                for value in mem_data:
                    fstring = "0x{:08X},\n".format(int(value) & 0xFFFFFFFF)
                    f.write(fstring)
        return mem_data
               
        

    def cpu_execution(self, log_opt = True, print_opt = True):
        # Création du fichier log
        if (log_opt == True):
            now = datetime.datetime.now()
            time_extension = now.strftime("%Y-%m-%d_%H-%M-%S-%f")  # Ajout de %f pour les microsecondes
            filename = "./log/"+time_extension+"_execution.txt"
            file = open(filename, 'w')
        
        self.mmio.write(0x0,0b00000000000000000000000000100000) # BOOT <= 1
        self.mmio.write(0x0,0b00000000000000000000000000000000) # BOOT <= 0
        for i in range(0, 500, 1):
            #Mode_debug  pour activé le CE : reg0(6)=1 & reg0(0)=1 => (0b00000000000000000000000001000001)
            #Mode_normal pour activé Le CE : reg0(6)=0 & reg0(0)=1 => (0b00000000000000000000000000000001)
            self.mmio.write(0x0,0b0000000000000000000000001000001)
            self.mmio.write(0x0,0b0000000000000000000000001000000)
            PC = self.mmio.read(0x10) # Sig_Adr_Inst_out
            Current_Ins = self.mmio.read(0x14) # Sig_Val_Out_Inst_out
            NextAdr_Ins = self.mmio.read(0x18) # Sig_New_Adr_Inst_out
            if print_opt:
                print("Program Counter (PC) value : ", PC, "(",int(PC/4),"), Current Instruction :", hex(Current_Ins) ,", New Address Instruction :", NextAdr_Ins,"\r")
            Mem_Data_Adr_Value = self.mmio.read(0x1C)
            Data_in  = self.mmio.read(0x20) # Sig_Val_In_Data_out
            Data_out = self.mmio.read(0x24) # Sig_Val_Out_Data_out
            if print_opt:
                print("Mem Data Address value : ", int(Mem_Data_Adr_Value) ,", Data In : ",hex(Data_in),", Data Out:",hex(Data_out)," \r");
            UAL_op = self.mmio.read(0x34)
            if print_opt:
                print("UAL operation: ",bin(UAL_op),"->",int(UAL_op),"\r")
            FSM_value = self.mmio.read(0x38)
            if print_opt:
                match int(FSM_value):
                    case 0:
                        FSM_value_str = "Init"
                        print("Current State Machine is : Init\r")
                    case 1:
                        FSM_value_str = "FetchIns"
                        print("Current State Machine is : FetchIns\r")
                    case 2: 
                        FSM_value_str = "Decode"
                        print("Current State Machine is : Decode\r")
                    case 3:
                        FSM_value_str = "ExeAddr"
                        print("Current State Machine is : ExeAddr\r")
                    case 4:
                        FSM_value_str = "ExeOp"
                        print("Current State Machine is : ExeOp\r")
                    case 5:
                        FSM_value_str = "ExeOpimm"
                        print("Current State Machine is : ExeOpimm \r")
                    case 6:
                        FSM_value_str = "ExeLoad"
                        print("Current State Machine is : ExeLoad \r")
                    case 7:
                        FSM_value_str = "ExeWrite"
                        print("Current State Machine is : ExeWrite\r")
                    case 8:
                        FSM_value_str = "ExeCtrr"
                        print("Current State Machine is : ExeCtrr\r")
                    case 9:
                        FSM_value_str = "ExeJal"
                        print("Current State Machine is : ExeJal\r")
                    case 10:
                        FSM_value_str = "ExeJalr2"
                        print("Current State Machine is : ExeJalr2\r")
                    case 11:
                        FSM_value_str = "ExeJalr"
                        print("Current State Machine is : ExeJalr\r")
                    case 12:
                        FSM_value_str = "Undefined"
                        print("Current State Machine is : Undefined\r\n\n")
                    case 13:
                        FSM_value_str = "ExeLui"
                        print("Current State Machine is : ExeLui\r")
                    case 14:
                        FSM_value_str = "ExeAuipc"
                        print("Current State Machine is : ExeAuipc\r")
                    case 15:
                        FSM_value_str = "ExeNop"
                        print("Current State Machine is : ExeNop\r")
                    case 16:
                        FSM_value_str = "ExeCordic1"
                        print("Current State Machine is : ExeCordic1\r")
                    case 17:
                        FSM_value_str = "ExeCordic2"
                        print("Current State Machine is : ExeCordic2\r")
                    case _ :
                        FSM_value_str = "Error"
                        print("Current State Machine is : Undefined\r\n\n")
            Date_UT_value = self.mmio.read(0x3C)
            if print_opt:
                print("Data in UT for Load Instruction",hex(Date_UT_value),",",bin(Date_UT_value),"\r\n")
            ################## LOG ########################################################
            if (log_opt == 1):
                file.write("---------------\ " +str(i) +" \---------------\n")
                file.write("Sig_Adr_Inst_out        :"+str(hex(PC))+"\n")
                file.write("Sig_Val_Out_Inst_out    :"+str(hex(Current_Ins))+"\n")
                file.write("Sig_New_Adr_Inst_out    :"+str(hex(NextAdr_Ins))+"\n")
                file.write("Sig_Adr_Mem_Data_out    :"+str(hex(Mem_Data_Adr_Value))+"\n")
                file.write("Sig_Val_In_Data_out     :"+str(hex(Data_in))+"\n")
                file.write("Sig_Val_Out_Data_out    :"+str(hex(Data_out))+"\n")
                # file.write("Sig_Jalr_Adr_out        :",+"\n")
                # file.write("Sig_Jr_Adr_out          :",+"\n")
                # file.write("Sig_br_jal_adr_out      :",+"\n")
                # file.write("Sig_sel_func_ALU_out    :"+UAL_op+"\n")
                file.write("Sig_FSM_state_out       :"+str(int(FSM_value))+" "+FSM_value_str+"\n")
                file.write("Sig_Val_Mem_Data_depth  :"+str(Date_UT_value)+"\n")
                file.write("\n\n")
        if (log_opt == 1):
            file.close()



    def cpu_run(self, time = 2):
        self.mmio.write(0x0,0b00000000000000000000000000100000) # BOOT <= 1
        self.mmio.write(0x0,0b00000000000000000000000000000000) # BOOT <= 0 
        self.mmio.write(0x0,0b0000000000000000000000000000001)
        sleep(time)
        self.mmio.write(0x0,0b0000000000000000000000000000001)
    
    def doc(self):
        print("https://github.com/FlorianCollin/RISCVEIRB_Controller")
        
    def tb_all(self, print_opt = False):
        self.tb("./tb/tb0", print_opt = print_opt)
        self.tb("./tb/tb1", print_opt = print_opt)
        
    def tb(self, tb_name, print_opt = False):
        print("TB : ", tb_name)
        inst_mem = charger_fichier(tb_name + ".hex")
        self.write_inst_mem_from_tab(inst_mem, inst_mem.size, print_opt = print_opt)
        self.cpu_execution(print_opt = print_opt)
        data_mem = self.read_data_mem(print_opt = print_opt);
        data_mem_check = charger_fichier(tb_name + "_mem.hex")
        count = 0
        for i in range(0, data_mem.size):
            # print("data_mem[", i, "]       = ", int(data_mem[i]), "       = ", hex(data_mem[i]))
            # print("data_mem_check[", i, "] = ", int(data_mem_check[i]), " = ", hex(data_mem_check[i]))
            if ((int(data_mem[i]) & 0xFFFFFFFF) != (int(data_mem_check[i]) & 0xFFFFFFFF)):
                print(tb_name, "[", i, "]", " failed !")
                print("data_mem[{}]= {:08X}\n".format(i, data_mem[i] & 0xFFFFFFFF))
                print("data_mem_check[{}]= {:08X}\n".format(i, data_mem_check[i] & 0xFFFFFFFF))
                count += 1
                
        if (count == 0):
            print(tb_name, " passed OK\n\n")
            return True
        else:
            print(tb_name, " failed !!")
            print(count, " error(s)")
            return False
         
        
        
        
        


 
## Fonctions utilitaires
def charger_fichier(path):
    if path.endswith('.hex'):
        with open(path, 'r') as file:
            data = np.array([int(line.strip().rstrip(','), 16) for line in file])
    else:
        print("Format de fichier non pris en charge.")
        return None
    return data