from pynq import MMIO
import numpy as np
import datetime
import os

class RISCVEIRB_Controller:

    
    def __init__(self, BASE_ADDRESS = 0x43C00000, ADDRESS_LENGTH = 0x64000):
        print("Création de la class RISCVEIRB_Controller")
        self.mmio = MMIO(BASE_ADDRESS, ADDRESS_LENGTH)


    ########## METHODES ##########
        
    ## WRITE ##

    def write_inst_mem_from_tab(self, mem_instruction, size = 32):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        CODE_RAM_SIZE = size
        print("\nInstruction Memory Write Process\n\r")
        for i in range(0, CODE_RAM_SIZE, 1):
            # Envoie octets par octets
            for j in range (0, 4, 1):
                adresse = (4 * i) + j
                tableauOctets[j]  = (mem_instruction[i] >> (j*8)) % 256;
                data_ins = ((0 << 24) + (tableauOctets[j] << 16) + 0b0000000000001010); # Inst_Boot & Inst_RW_Boot
                # Ecriture dans la mémoire octets par octets
                self.mmio.write(0x04, adresse)
                self.mmio.write(0x00, int(data_ins))
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
                self.mmio.write(0x00, int(data_val))
            print("Octet value Write for current Instruction",hex(mem_data[i]),"at address", i,": [",hex(tableauOctets[3]),";",hex(tableauOctets[2]),";",hex(tableauOctets[1]),";",hex(tableauOctets[0]),"]")
    

    ## READ ##

    def read_inst_mem(self, size = 32, log_opt = False, file_name = "inst_mem"):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        mem_instruction = np.zeros(size)
        CODE_RAM_SIZE = size
        #Instruction Memory Read Process  
        print("\nInstruction Memory Read Process\n\r")
        for i in range(0, CODE_RAM_SIZE, 1):
            for j in range (0, 4, 1):
                # Sequence lecture
                # Inst_RW_Boot <= 0 (READ)
                # Inst_Boot <= 1 
                self.mmio.write(0x00,0b00000000000000000000000000000010)
                adresse = ((4 * i) + j)
                self.mmio.write(0x04, adresse)
                tableauOctets[j] = self.mmio.read(0xC)>>16
                data_ins_rd = (tableauOctets[3] << 24) + (tableauOctets[2] << 16) + (tableauOctets[1] << 8) + (tableauOctets[0]) 
            if (data_ins_rd < 0) : 
                data_ins_rd = (data_ins_rd + (1<<32))
            print("La valeur de l'instruction", i," est :", hex(data_ins_rd))
            mem_instruction[i] = data_ins_rd
         # Enregistrement dans un fichier log    
        if (log_opt):
            now = datetime.datetime.now()
            time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")  # Ajout de %f pour les microsecondes
            log_file_name = "./log/"+time+"_"+file_name+".hex"
            with open(log_file_name, 'w') as f:
                for value in mem_instruction:
                    f.write(f'0x{int(value):08X},\n')
                   
            

    
    def read_data_mem(self, size = 32, log_opt = False, file_name = "data_mem"):
        tableauOctets = np.array([0x00, 0x00, 0x00, 0x00])
        mem_data = np.zeros(size)
        CODE_RAM_SIZE = size
        #Data Memory Read Process  
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
            if (data_val_rd  < 0) : 
                data_val_rd  = (data_val_rd  + (1<<32))
            mem_data[i] = int(data_val_rd)
            print("La valeur de la donnée", i," est :", hex(data_val_rd))
        # Enregistrement dans un fichier log    
        if (log_opt):
            now = datetime.datetime.now()
            time_extension = now.strftime("%Y-%m-%d_%H-%M-%S-%f")  # Ajout de %f pour les microsecondes
            filename = "./log/"+time_extension+"_"+file_name+".hex"
            with open(filename, 'w') as f:
                for value in mem_data:
                    f.write(f'0x{int(value):08X},\n')

    
    
#################################################################################################
                        
#################################################################################################

def charger_fichier(path):
    if path.endswith('.hex'):
        with open(path, 'r') as file:
            data = np.array([int(line.strip().rstrip(','), 16) for line in file])
    else:
        print("Format de fichier non pris en charge.")
        return None
    return data