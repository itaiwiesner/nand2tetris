// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// R1 is being used as the index

    // initialize R2. RAM[R2] = 0
    @R2
    M=0
    // initialize i (index). i = RAM[R1]
    @R1
    D=M
    @i
    M=D

(LOOP)
    // if (RAM[R1] == 0) goto END
    @i
    D=M
    @END
    D;JEQ

    // decrease i by 1. RAM[i] = RAM[i] - 1
    @i
    M=M-1
    
    // increase R2 by R0. RAM[R2] = RAM[R2] + RAM[R0]
    @R0
    D=M
    @R2
    M=M+D

    // goto LOOP
    @LOOP
    0;JMP

(END)
    @END
    0;JMP
