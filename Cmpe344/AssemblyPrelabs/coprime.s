.globl _start

.equ M, 7

.data
D: .word 5,7,0, 8,24,0, 11,44,0, 11,18,0, 36,2,0, 63,27,0, 19,24,0

.text
gcd:

# Insert gcd function below.

  mv t0, a0                                         # t0 = A, first arg of function
  mv t1, a1                                         # t1 = B, second arg of function
  sub t2, t0, t1                                    # t2 = A - B. t2 will keep abs. value of difference
  mv t6, t0                                         # in case A == B
  mv t4, zero                                       # t4 = 0, loop counter
  blt zero, t2, GCD                                 # if zero < t2, continue
  sub t2, t1, t0                                    # else t2 = B - A

GCD:
  beq t4, t2, GCD_DONE                              # if difference == loop count, done
  addi t4, t4, 1
  rem t5, t0, t4                                    # t5 = remainder
  bne zero, t5, GCD
  rem t5, t1, t4
  bne zero, t5, GCD
  mv t6, t4                                         # t6 keeps gcd
  j GCD

GCD_DONE:
  mv a0, t6                                         # a0 = x10, return register keeps gcd value.

# Insert gcd function above.

	ret

coprime:

# Insert coprime function below.

  addi sp, sp, -16                                  # prologue part:
  sw s0, 0(sp)
  sw s1, 4(sp)
  sw s2, 8(sp)
  sw ra, 12(sp)

  mv s0, zero                                       # s0 = how many times we called gcd. when equals M, exit from loop
  li s1, M
  la s2, D                                          # keeps address of D array

LOOP:
  bge s0, s1, LOOP_DONE
  lw a0, (s2)                                       # a0 = x10, func arg 0
  lw a1, 4(s2)										# a1 = x11, func arg 1

  jal gcd                                           # call gcd with a0, a1 parameters
  li t0, 1                                          # to store array's third elem 1 or 2 depending on the result from gcd
  mv t1, a0                                         # to store return value of gcd function
  beq t1, t0, LOOP_ELSE                             # if return value of gcd == 1, go LOOP_ELSE. x10 = a0, return value
  add t0, t0, 1                                     # else add 1.
LOOP_ELSE:
  sw t0, 8(s2)
  addi s0, s0, 1
  addi s2, s2, 12
  j LOOP

LOOP_DONE:
  lw s0, 0(sp)                                      # epilogue part:
  lw s1, 4(sp)
  lw s2, 8(sp)
  lw ra, 12(sp)
  addi sp, sp, 16

# Insert coprime function above.

	ret

_start:

# Insert _start function below.
  jal coprime

# Insert _start function above.

	ret

.end

