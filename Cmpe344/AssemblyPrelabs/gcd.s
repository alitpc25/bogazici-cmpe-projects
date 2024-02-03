.globl _start                     # Make _start symbol visible outside

.equ A, 192                
.equ B, 216                

.section .text                    # .text is a read-only section containing executable code (abbreviated as .text)
_start:                           # _start symbol is special, the program starts here
  li t0, A              # t0 = A
  li t1, B              # t1 = B
  sub t2, t0, t1        # t2 = A - B. t2 will keep abs. value of difference
  mv t6, A              # in case A == B
  blt zero, t2, GCD     # if zero < t2, continue
  sub t2, t1, t0        # else t2 = B - A
  mv t4, zero           # t4 = 0, loop counter

GCD:
  beq t4, t2, GCD_DONE
  addi t2, t2, 1
  rem t5, t0, t2        # t5 = remainder
  bne zero, t5, GCD
  rem t5, t1, t2
  bne zero, t5, GCD
  mv t6, t2
  

GCD_DONE:
  mv t6, t6
  j .