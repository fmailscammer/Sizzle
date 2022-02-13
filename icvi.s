;; Setup (clear stack and mem)
304 307
;; Move to stack 9 and store 'cvi.s' on stack for later.
409
099 010 010 102 018 100 010 010 102 005 100 046 010 010 102 015 100
;; Start label (for looping)
@ST
;; Move to stack 1 and copy 'cvi.s', and then move it onto mem
401 439 310 308
203
;; Move to stack 2 (an empty stack, not really necessary but more fun) and run it
402 207
;; Go back to the beginning of the program
$ST