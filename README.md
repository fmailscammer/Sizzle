# Sizzle

Sizzle is an esoteric language, inspired by [Burn](https://esolangs.org/wiki/Burn) because I thought that it looked cool. Hopefully this language won't become a mystery that nobody knows how to solve like burn did.

This language is stack based, but it might have variables with names at some point.

## Basics
Code is a series of blocks made up of 3 characters such as
```
001 002 100 201
```
These blocks are broken into two parts:  
```
         0|01  
         ^|^^  
Identifier|Value
```
The first part is an identifier for what type of block it is. The second part is its value. For this block, the '0' means push to stack, and the '01' is the number that it will push.
The second block is the same, but this time it adds a 2.

The block '100' has an identifier of 1, meaning operator. The value '00' means addition, so it will pop the top two values from the stack, add them, and then push the result onto the stack.

The last block, '201' has an identifier of 2, and a value of '01'. The '2' identifier is for user I/O, and the '01' means output number. This outputs the top value from the stack as a number instead of as an ascii code.

For a more detailed explanation, see Commands.  
For a detailed list of all commands and what they do, see Operations or Operations List (near the bottom of the page)

### Example programs:

Here is a program that prints `Hello, world!`, with comments to show what it is doing.
```
;; Add H code 72
072
;; Add e code 101
010 010 102 001 100
;; Add ll code 108 108
010 010 102 008 100 301
;; Add o code 11
010 010 102 011 100
;; Add , code 44
044
;; Add space code 32
032
;; Add w code 119
010 010 102 019 100
;; Add o code 11
010 010 102 011 100
;; Add r code 114
010 010 102 014 100
;; Add l code 108
010 010 102 008 100
;; Add d code 100
010 010 102
;; Add ! code 33
033
;; Reverse stack and move stack into mem
308 306
;; Print
203
;; Clear stack and mem
;; This line isn't necessary, but cleaning up after yourself is good in larger programs
302 305
```

## Details

### The stack

The stack is just a list of values that is always accessed from top to bottom.
Trying to pop from an empty stack will result in an error. There is technically no limit to how large the stack can be, but eventually the computer will run out of memory.

Because of how much of a pain stacks are, in Sizzle you actually have access to up to 10 stacks. They are all initialized as empty, and by default stack 0 is active. A program can switch active stacks and do operations between stacks with the `4` identifier and its subcommands.

### Mem

You also have access to a single memory slot called 'mem'. It has a special set of commands to access it. It can be useful for storing strings, as it doesn't have a length limit, while the stack has a limit of storing one number per slot.

Many commands are heavily reliant on mem because of the lack of support for strings in the stack.

**All values moved into mem are converted from numbers to the ASCII values corresponding to those numbers. If a number is not a valid ASCII code, an error will be thrown.**

### Commands

Each command is made up of an identifier and a value, as shown above. This section includes the details of every identifier that has been implemented and all of its subcommands, but first some examples:  

#### Caveat Alert: Values can only be 2 characters long. This means that in order to use numbers that aren't 0-99 you must use a combination of operations to create numbers that are outside of this range. For example, to create 153, we could do: `015 010 102 003 100`, which:
- Pushes 15 and 10 to the stack (stack:[15, 10]) 
- Multiplies them together (stack:[150])  
- Pushes 3 to the stack (stack:[150, 3])  
- Adds them, leaving 153 (stack:[153])  

### Operations:

*(Replace \* with a number)*

0. Push to stack  
  \*\*: Push value \*\* to the stack (`010` will push `10` onto the stack). 
1. Math and Logic Operations  
  00: Add  
  01: Subtract  
  02: Multiply  
  03: Divide  
  04: Exponent  
  05: Modulo  
  06: Equal  
  07: Greater than  
  08: Less than  
  09: Greater than or equal to  
  10: Less than or equal to  
2. I/O (and other connections to the outside world)  
  00: Input with prompt from `mem` into `mem`  
  01: Output top item in stack as a number  
  02: Output top item in stack as ASCII value  
  03: Output `mem` (as string)  
  04: Exit with code 0
  05: Exit with code 1  
  06: Exit with code of top value from stack  
  07: Run file with name stored in `mem`
3. Stack <-> mem commands  
  00: Discard top item from stack (\[...,1, 2\] -> \[..., 1\])  
  01: Duplicate top item of stack (\[..., 1\] -> \[..., 1, 1\])  
  02: Swap top two items of stack  
  03: Rotate top three items of stack (1, 2, 3) -> (2, 3, 1)  
  04: Clear stack (\[...\] -> \[\])  
  05: Pop from stack into `mem` as ASCII value  
  06: Push from `mem` onto stack  
  07: Clear `mem`  
  08: Move stack into `mem` (leaves stack empty)  
  09: Move `mem` into stack (leaves `mem` empty)  
  10: Reverse stack  
  11: Reverse `mem`  
  12: Push length of active stack to active stack  
  13: Push length of `mem ` to active stack  
  14: Move top item of stack into mem as string  
4. Multi-Stack commands  
  0\*: Switch active stack to \*  
  1\*: Pop `top` value from stack \* onto active stack  
  2\*: Append stack \* to active stack  
  3\*: Replace current stack with stack \*  
  4\*: Clear stack \*  
  
Identifiers `4` is a special case, because these commands actually get an identifier *and* a value from the value of the main command. Example:
```
401
4                 0                1
Main identifier | Sub identifier | Value
```
This would have identifier `4` (Multi-Stack commands), sub-identifier `0` (Switch active stack to value) and value `1`, which means it will switch the active stack to stack `1`.

###  All Operations
That other section might get a bit confusing, so this is just a section with every single command because I *love* redundancy

0\*\* : Push value \*\* onto the stack  

100: Pop top two numbers, add them, and push result to the stack  
101: Pop top two numbers, subtract `top` from `second from top` value, and push result to the stack  
102: Pop top two numbers, multiply them, and push result to the stack  
103: Pop top two numbers, divide `second from top` by `top`, and push result to the stack  
104: Pop top two numbers, raise `second from top` value to `top` value, and push result to stack  
105: Pop top two numbers, get remainder of `second from top` divided by `top` and push result to stack  
106: Pop top two numbers, check if they are equal, and push `1` for true and `0` for false  
107: Pop top two numbers, check if `second to top` is greater than `top` and push result  
108: Pop top two numbers, check if `second to top` is less than `top` and push result  
109: Pop top two numbers, check if `second to top` is great than or equal to `top` and push result  
110: Pop top two numbers, check if `second to top` is less than or equal to `top` and push result  

200: Input with prompt `mem` and set `mem` to result  
201: Print `top` item of stack as a number  
202: Print `top` item of stack as a char with number's ASCII code  
203: Print `mem` (as string)  
204: Exit with code `0`  
205: Exit with code `1`  
206: Exit with `top` value of stack as exit code  
207: Run file with name in `mem`  

300: Discard `top` item of stack  
301: Duplicate `top` item of stack  
302: Swap top two items of stack  
303: Rotate top 3 items of stack (A, B, C) -> (B, C, A)  
304: Clear active stack  
305: Pop `top` value of stack and append it to `mem`  
306: Push from `mem` onto stack  
307: Clear `mem`  
308: Move entire stack into `mem` (leaves stack empty)  
309: Move `mem` into stack (leaves `mem` empty)  
310: Reverse stack  
311: Reverse `mem`  
312: Push length of active stack to active stack  
313: Push length of `mem  ` to active stack  
314: Move top item of stack into `mem` (as string instead of ASCII)

40\*: Switch active stack to \*  
41\*: Pop `top` value from stack \* and push it onto active stack  
42\*: Append stack * to active stack (doesn't modify stack \*)  
43\*: Replace active stack with stack \*  
44\*: Clear stack \*  
45\*: Push length of stack \* to current stack  