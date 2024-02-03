.globl _start             # Make _start symbol visible outside

.equ ARR_SIZE, 10         # Set ARR_SIZE to 10. Last element of array is 0, dont take it.
.equ LOOP_COUNT, 8        # Set LOOP_COUNT to ARR_SIZE - 2.
                     
.section .data          # .data is a read-only section containing global static data (abbreviated as .data)
V: .word 42,35,33,29,17,11,8,6,3,0

.section .text            # .text is a read-only section containing executable code (abbreviated as .text)
_start:                        
  li t2, LOOP_COUNT    #outer loop count   

OUTER_LOOP:
  beq t2, zero, OUTER_LOOP_DONE
  la t0, V                
  mv t1, t2    #inner loop count

INNER_LOOP:
  beq t1, zero, INNER_LOOP_DONE
  lw t3, (t0)
  lw t4, 4(t0)
  blt t3, t4, CONT
  # swap case
  mv t5, t3
  sw t4, (t0)
  sw t5, 4(t0)

CONT:
  add t0, t0, 4
  add t1, t1, -1
  j INNER_LOOP

INNER_LOOP_DONE:
  add t2, t2, -1
  j OUTER_LOOP

OUTER_LOOP_DONE:
  j . 