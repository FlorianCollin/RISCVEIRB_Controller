# Documentation du Projet

- [Documentation du Projet](#documentation-du-projet)
  - [MMIO MEMO](#mmio-memo)
  - [CPU\_RISCV port mapping :](#cpu_riscv-port-mapping-)
  - [Component CPU\_RISCV](#component-cpu_riscv)


## MMIO MEMO

| loc_addr | addr_off(MMIO) | cpu_riscv_port (32 bits) |
| -------- | -------------- | ------------------------ |
| b"0000"  | 0x00           | slv_reg0                 |
| b"0001"  | 0x04           | slv_reg1                 |
| b"0010"  | 0x08           | slv_reg2                 |
| b"0011"  | 0x0c           | val_mem                  |
| b"0100"  | 0x10           | Sig_Adr_Inst_out         |
| b"0101"  | 0x14           | Sig_Val_Out_Inst_out     |
| b"0110"  | 0x18           | Sig_New_Adr_Inst_out     |
| b"0111"  | 0x1c           | Sig_Adr_Mem_Data_out     |
| b"1000"  | 0x20           | Sig_Val_In_Data_out      |
| b"1001"  | 0x24           | Sig_Val_Out_Data_out     |
| b"1010"  | 0x28           | Sig_Jalr_Adr_out         |
| b"1011"  | 0x2c           | Sig_Jr_Adr_out           |
| b"1100"  | 0x30           | Sig_br_jal_adr_out       |
| b"1101"  | 0x34           | Sig_sel_func_ALU_out     |
| b"1110"  | 0x38           | Sig_FSM_state_out        |
| b"1111"  | 0x3c           | Sig_Val_Mem_Data_depth   |



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

<!-- ## Non utilisés :
```vhdl
constant cst16    : std_logic_vector(15 downto 0) := x"ABCD";
val_mem(15 downto 0) <= cst16;
Sig_sel_func_ALU_out(31 downto 4) <= "0000000000000000000000000000";
Sig_FSM_state_out(31 downto 5)    <= "000000000000000000000000000";
```  -->
