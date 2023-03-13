// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(MAIN)
    @SCREEN
    D=M

    // pointer that stores the current 16 pixels we are working on
    @current
    M=D

    // check if any key is pressed
    @KBD
    D=M

    @WHITE
    D;JEQ

    @BLACK
    0;JMP

(BLACK)
    @color
    M=-1
    @DRAW
    0;JMP

(WHITE)
    @color
    M=0
    @DRAW
    0;JMP


(DRAW)
    @color // D = color stored in RAM[color]
    D=M

    @R2 // RAM[R2] = SCREEN + current pixel's index
    A=M // goto current pixel
    M=D

    @R2
    M=M+1 // RAM[R2] += 1
    D=M // D = SCREEN + next pixel's index 

    @KEYBOARD
    D=A-D // Set D to be KEYBOARD- (SCREEN + pixel's index)

    @DRAW
    D;JGE

    @MAIN
    0;JMP
