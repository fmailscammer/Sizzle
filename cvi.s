;; Add 100 code to stack 1 and back to stack 0
401
048 049 048 032 048 049 048 032 049 048 050 032
400
;; Make prompt and get input (leave a 0 behind for looping later)
304 307 061 062 032 310 308
000 200
;; Move input into stack
309

;; For every item in the input (which is in stack 0):
;; Check if it is >= 100: Do fancy thing [IGNORE FOR NOW]
;; If it is < 100: Move into register 2 (output), convert to string, and move back one by one

;; Start of loop
@L_
;; Move to stack 0 (the input)
400
;; Duplicate so we can use it after checking if its >= 100
301 301 301
;; Check if number is not 0 (null character that ends input text)
000 107 ?NZ $EN
;; NZ label for if number is not zero
@NZ
;; Check if it is >= 100
099 001 100 109 ?GH
;; If it is not >= 100, goto LH
$LH
;; Re-entry point from @GH and @LH
@RE
402
032
400
;; Check if there is any value left, otherwise go to the end.
?L_
$EN

;; It is GREATER THAN OR EQUAL TO 100
@GH
;; Clear memory and move to 2 (the output stack)
307 402
;; Move in the ASCII for a 100 from stack 1
421
;; Take the value from 0 (input)
410
;; Subtract 100
099 001 100 101
;; Move our new subtracted number into mem and reverse it
314 311
;; Check if mem is 1 or 2 characters long
313 001 106 ?M1 $M2

;; mem is 1 character long
@M1
;; Add 2 0s and then the value from mem
048 048 306
$AD

;; mem is 2 characters long
@M2
;; Add 1 0 and then the values from mem
048 306 306
$AD

;; add in the addition to combine the 100 with the new value
@AD
032 049 048 048
$RE

;; It is LESS THAN 100
@LH
;; Clear memory and move to 2 (the output stack)
307 402
;; Move value from stack 0 to stack 2 and move it into mem as string
410 314
;; Reverse mem and move both digits from mem back into stack 2 (with 0s for the push stack command)
048 311 306 306
$RE

;; End of file (runs after the loop completes)
@EN
402
310
308 203
304 307