.globl _start                     # Make _start symbol visible outside

.equ ARR_SIZE, 10                 # Set ARR_SIZE to 10. Last element of array is 0, dont take it.
.equ LOOP_COUNT, 8                # Set LOOP_COUNT to ARR_SIZE - 2.
                     
.section .data                    # .data is a read-only section containing global static data (abbreviated as .data)
V: .word 42,35,33,29,17,11,8,6,3,0

.section .text                    # .text is a read-only section containing executable code (abbreviated as .text)
_start:                           # _start symbol is special, the program starts here
  li t2, LOOP_COUNT               # Register `t2` keeps the loop index, initially set to LOOP_COUNT

OUTER_LOOP:
  beq t2, zero, OUTER_LOOP_DONE   # if the number of outer loops is reached goto OUTER_LOOP_DONE
  la t0, V                        # Register `t0` keeps the address of the array index initially V[0].                         
  mv t1, t2                       # Inner loop count: loop index

INNER_LOOP:
  beq t1, zero, INNER_LOOP_DONE   # if the number of inner loops is reached goto INNER_LOOP_DONE
  lw t3, (t0)
  lw t4, 4(t0)                    # Register t3 and t4 keeps two adjacent values ​​to be compared in order
  blt t3, t4, CONT                # No need for swap if t3 is less than t4
  # swap case
  mv t5, t3
  sw t4, (t0)
  sw t5, 4(t0)

CONT:
  add t0, t0, 4                   # next index
  add t1, t1, -1                  # t1--
  j INNER_LOOP                    # Jump INNER_LOOP label unconditionally and continue loop

INNER_LOOP_DONE:
  add t2, t2, -1                  # t2--
  j OUTER_LOOP                    # Jump OUTER_LOOP label unconditionally and continue loop

OUTER_LOOP_DONE:
  j .