//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D-M
M=-1
@EQ0
D;JEQ
@SP
A=M-1
M=0
EQ0
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D-M
M=-1
@EQ1
D;JEQ
@SP
A=M-1
M=0
EQ1
//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D-M
M=-1
@EQ2
D;JEQ
@SP
A=M-1
M=0
EQ2
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@LT3
D;JLT
@SP
A=M-1
M=0
LT3
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@LT4
D;JLT
@SP
A=M-1
M=0
LT4
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@LT5
D;JLT
@SP
A=M-1
M=0
LT5
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@GT6
D;JGT
@SP
A=M-1
M=0
GT6
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@GT7
D;JGT
@SP
A=M-1
M=0
GT7
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
M=-1
@GT8
D;JGT
@SP
A=M-1
M=0
GT8
//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
//neg
@SP
A=M-1
M=-M
//and
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D&M
//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
//or
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D|M
//not
@SP
A=M-1
M=!M
