# Documentation du Projet

- [Documentation du Projet](#documentation-du-projet)
  - [RISCVEIRB](#riscveirb)
  - [MMIO MEMO](#mmio-memo)
  - [CPU\_RISCV port mapping :](#cpu_riscv-port-mapping-)
  - [Component CPU\_RISCV](#component-cpu_riscv)
  - [Documentation de la classe RISCVEIRB\_Controller (liste des méhtodes)](#documentation-de-la-classe-riscveirb_controller-liste-des-méhtodes)

## RISCVEIRB

RISCVEIRB est un processeur rv32i développé par les étudiants de l'Enseirb Matmeca. Pour tester ce processeur, nous utilisons une carte de développement Pynq.

Les cartes Pynq permettent la création d'overlays, ce qui nous permet de contrôler facilement un design (ici un CPU) depuis un langage tel que Python. Pour plus d'informations sur les cartes Pynq, consultez la [documentation Zynq](https://pynq.readthedocs.io/en/v2.4/getting_started.html).

Ce projet est lié à un autre de mes projets : [RISCV-CORDIC-toolchain](https://github.com/FlorianCollin/RISCV-CORDIC-toolchain), qui étend le jeu d'instructions avec des instructions de calcul trigonométrique (CORDIC). Dans ce projet, vous trouverez le fichier shell `stohex.sh`, qui permet de créer facilement un programme (.hex) à charger dans la mémoire d'instruction.

L'objectif de ce projet est de créer une couche logicielle (en Python) permettant de simplifier l'envoi de données sur les mémoires du processeur ainsi que leur lecture. De plus, nous pourrons lire des signaux préalablement créés pour le débogage.

Le code Python repose principalement sur la classe MMIO. Pour en savoir plus sur MMIO, consultez la [documentation MMIO](https://pynq.readthedocs.io/en/v2.4/pynq_libraries/mmio.html).

Dans ce dépôt, vous trouverez le fichier `RISCVEIRB_Controller.py`, des notebooks Jupyter, ainsi que des fichiers de test hexadécimaux pour tester la classe et le CPU.

## MMIO MEMO

| addr_off(MMIO) | cpu_riscv_port (32 bits) |
| -------------- | ------------------------ |
| 0x00           | slv_reg0                 |
| 0x04           | slv_reg1                 |
| 0x08           | slv_reg2                 |
| 0x0c           | val_mem                  |
| 0x10           | Sig_Adr_Inst_out         |
| 0x14           | Sig_Val_Out_Inst_out     |
| 0x18           | Sig_New_Adr_Inst_out     |
| 0x1c           | Sig_Adr_Mem_Data_out     |
| 0x20           | Sig_Val_In_Data_out      |
| 0x24           | Sig_Val_Out_Data_out     |
| 0x28           | Sig_Jalr_Adr_out         |
| 0x2c           | Sig_Jr_Adr_out           |
| 0x30           | Sig_br_jal_adr_out       |
| 0x34           | Sig_sel_func_ALU_out     |
| 0x38           | Sig_FSM_state_out        |
| 0x3c           | Sig_Val_Mem_Data_depth   |



## CPU_RISCV port mapping :

| Port                 | Largeur (bits) | Correspondance                   |
| -------------------- | -------------- | -------------------------------- |
| Clk                  | 1              | S_AXI_ACLK                       |
| Reset                | 1              | RESET                            |
| CE                   | 1              | slv_reg0(0)                      |
| Inst_Boot            | 1              | slv_reg0(1)                      |
| Data_Boot            | 1              | slv_reg0(2)                      |
| Inst_RW_Boot         | 1              | slv_reg0(3)                      |
| Data_RW_Boot         | 1              | slv_reg0(4)                      |
| Boot                 | 1              | slv_reg0(5)                      |
| Debug                | 1              | slv_reg0(6)                      |
| Val_Inst_In_boot     | 8              | slv_reg0(23 downto 16)           |
| Val_Data_In_boot     | 8              | slv_reg0(31 downto 24)           |
| Adr_Inst_boot        | 32             | slv_reg1                         |
| Adr_Data_boot        | 32             | slv_reg2                         |
| Val_Inst_Out_Boot    | 8              | val_mem(23 downto 16)            |
| Val_Data_Out_Boot    | 8              | val_mem(31 downto 24)            |
| Sig_Adr_Inst_out     | 32             | Sig_Adr_Inst_out                 |
| Sig_Val_Out_Inst_out | 32             | Sig_Val_Out_Inst_out             |
| Sig_New_Adr_Inst_out | 32             | Sig_New_Adr_Inst_out             |
| Sig_Adr_Mem_Data_out | 32             | Sig_Adr_Mem_Data_out             |
| Sig_Val_In_Data_out  | 32             | Sig_Val_In_Data_out              |
| Sig_Val_Out_Data_out | 32             | Sig_Val_Out_Data_out             |
| Sig_Jalr_Adr_out     | 32             | Sig_Jalr_Adr_out                 |
| Sig_Jr_Adr_out       | 32             | Sig_Jr_Adr_out                   |
| Sig_br_jal_adr_out   | 32             | Sig_br_jal_adr_out               |
| Sig_sel_func_ALU_out | 4              | Sig_sel_func_ALU_out(3 downto 0) |
| FSM_state            | 5              | Sig_FSM_state_out(4 downto 0)    |
| Val_Mem_Data_depth   | 32             | Sig_Val_Mem_Data_depth           |



## Component CPU_RISCV

```vhdl
component CPU_RISCV is
    Generic(
           Bit_Nber    : INTEGER    := 32;
           Memory_size : INTEGER    := 7
           );
    Port ( Clk               : in STD_LOGIC;
           Reset             : in STD_LOGIC;
           CE                : in STD_LOGIC;
           boot              : in STD_LOGIC;
           Debug             : in STD_LOGIC;
           Inst_Boot         : in STD_LOGIC;
           Data_Boot         : in STD_LOGIC;
           Inst_RW_Boot      : in STD_LOGIC;
           Data_RW_Boot      : in STD_LOGIC;
           Adr_Inst_boot     : in STD_LOGIC_VECTOR  ((Bit_Nber -1) downto 0);
           Adr_Data_boot     : in STD_LOGIC_VECTOR  ((Bit_Nber -1) downto 0);
           Val_Inst_In_boot  : in STD_LOGIC_VECTOR  ((8-1) downto 0);
           Val_Data_In_boot  : in STD_LOGIC_VECTOR  ((8-1) downto 0);           
           Val_Inst_Out_Boot : out STD_LOGIC_VECTOR ((8-1) downto 0);           
           Val_Data_Out_Boot : out STD_LOGIC_VECTOR ((8-1) downto 0);
           
           Sig_Adr_Inst_out     : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_Val_Out_Inst_out : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_New_Adr_Inst_out : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_Adr_Mem_Data_out : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_Val_In_Data_out  : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_Val_Out_Data_out : out STD_LOGIC_VECTOR (31 downto 0);
           Sig_Jalr_Adr_out     : out STD_LOGIC_VECTOR (31 downto 0); 
           Sig_Jr_Adr_out       : out STD_LOGIC_VECTOR (31 downto 0); 
           Sig_br_jal_adr_out   : out STD_LOGIC_VECTOR (31 downto 0); 
           Sig_sel_func_ALU_out : out STD_LOGIC_VECTOR (3 downto 0);
           FSM_state            : out STD_LOGIC_VECTOR (4 downto 0);
           Val_Mem_Data_depth : out STD_LOGIC_VECTOR ((Bit_Nber-1) downto 0)         
           );
   end component;

``` 


## Documentation de la classe RISCVEIRB_Controller (liste des méhtodes)

- `__init__(BASE_ADDRESS=0x43C00000, ADDRESS_LENGTH=0x64000)`: 
  - Constructeur de la classe 
  - Initialise une nouvelle instance de RISCVEIRB_Controller.
  
- `write_inst_mem_from_tab(mem_instruction, size=32)`:
  -  Écrit dans la mémoire d'instructions à partir d'un tableau. (numpy)
  -  Pour charger un fichier dans un tableau numpy, utiliser `charger_fichi`r`
  
- `write_data_mem_from_tab(mem_data, size=32)`:
  -  Écrit dans la mémoire de données à partir d'un tableau. (numpy)
  
- `read_inst_mem(size=32, log_opt=True, file_name="inst_mem")`:
  -  Lit la mémoire d'instructions.
  
- `read_data_mem(size=32, log_opt=True, file_name="data_mem")`:
  -  Lit la mémoire de données.
  
- `cpu_execution(log_opt=True)`:
  - Exécute le processeur.

- `cpu_run(time = 2)`: 
  - Lance l'exécution du processeur.
  - Par défault le cpu tourne pendant 2 secondes
  
- `doc()`:
  - Affiche la documentation du module. (lien vers github)
  
- `tb_all()`: 
  - Exécute les tests benchmarck. Ne pas utiliser autrement que pour du débugage !
  
- `tb(tb_name)`: 
  - Exécute un test benchmarck spécifique.
  - exemple : tb("../tb/tbcos", plot_opt = True) NE PAS METTRE L'EXTENSION DE FICHIER (.hex)
  - ATTENTION : Il faut respecter le formalisme imposer par la fonciton**, exemple de structure :
    - tbx.hex
    - tbx_mem.hex

- `slv_reg0_creat(CE, Inst_Boot, Data_Boot, Inst_RW_Boot, Data_RW_Boot, Boot, Val_Inst_In_boot, Val_Data_In_Boot)`:
  -  Crée la valeur pour le registre de contrôle slv_reg0.
  -  Il s'agit d'une méthode interne.

On retrouve différentes options de méthodes :
- plot_opt pour activer ou non l'ecriture des commentaires sur la sortie standard
- log_opt pour activer ou non l'écriture des commentaires dans un fichier log (/log).

Pout charger un fichier .hex en tableau numpy utiliser `charger_fichier(filename)`

**Pour rester cohérent avec la classe vous devez :**
- Créer un dossier (à la racine de jupyter) `/tb` pour les testbench (tbx.hex et tbx_mem.hex).
- Créer un dossier `/log` pour ranger les logs produits par les méhtodes de la classe RISCVERIB_Controller.

N'hesitez pas à modifier la classe qui n'est pas parfaite, elle a cependant le mérite d'être un bon point de départ dans la création d'une classe de test pour notre processeur RISCVEIRB_Controller.

  