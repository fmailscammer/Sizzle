import re

# Setup
stacks = [[] for i in range(10)]
current_stack = 0
mem = ""

# Commands
def pushstack(value):
  stacks[current_stack].append(int(value))
  return value

def op(value):
  global stacks
  global current_stack

  if value == '11':
    val = stacks[current_stack].pop()
    if val:
      stacks[current_stack].append(0)
    else:
      stacks[current_stack].append(1)
    return True

  ops = {
    '00': lambda a, b: a + b,
    '01': lambda a, b: a - b,
    '02': lambda a, b: a * b,
    '03': lambda a, b: a / b,
    '04': lambda a, b: a ** b,
    '05': lambda a, b: a % b,
    '06': lambda a, b: int(a == b),
    '07': lambda a, b: int(a > b),
    '08': lambda a, b: int(a < b),
    '09': lambda a, b: int(a >= b),
    '10': lambda a, b: int(a <= b),
  }

  b, a = stacks[current_stack].pop(), stacks[current_stack].pop()

  if not value in ops:
    return None

  op_ = ops[value]
  stacks[current_stack].append(op_(a, b))

  return True

def io(value):
  global mem
  def input_():
    global mem

    mem = str(input(mem))
    return mem

  def print_():
    print(stacks[current_stack][-1])
    return stacks[current_stack][-1]
  
  def print_asci():
    print(chr(stacks[current_stack][-1]), end="")
    return stacks[current_stack][-1]
  
  def print_mem():
    print(mem)
    return mem
  
  def run_mem():
    fn = mem

    with open(fn, "r") as f:
      code = f.read()
    
    new_exec = Executor(code)
    result, error = new_exec.run()
    if error:
      print("error!")
      print(error)

    return True
  
  def print_whole_stack():
    print(stacks[current_stack])

  funcs = {
    '00': input_,
    '01': print_,
    '02': print_asci,
    '03': print_mem,
    '04': lambda: exit(0),
    '05': lambda: exit(1),
    '06': lambda: exit(stacks[current_stack][-1]),
    '07': run_mem,
    '08': print_whole_stack,
  }

  if not value in funcs:
    return None

  func = funcs[value]
  func()

  return True

def stackmemcommands(value):
  global mem

  def discard():
    return stacks[current_stack].pop()
  
  def duplicate():
    stacks[current_stack].append(stacks[current_stack][-1])
    return stacks[current_stack][-1]
  
  def rotate_top_2():
    stacks[current_stack][-1], stacks[current_stack][-2] = stacks[current_stack][-2], stacks[current_stack][-1]
  
  def rotate_top_3():
    stacks[current_stack][-3], stacks[current_stack][-2], stacks[current_stack][-1] = stacks[current_stack][-2], stacks[current_stack][-1], stacks[current_stack][-3]
  
  def clear_stack():
    stacks[current_stack] = []
    return stacks[current_stack]
  
  def pop_to_mem():
    global mem

    mem += chr(stacks[current_stack].pop())
    return mem[-1]
  
  def push_from_mem():
    global mem

    stacks[current_stack].append(ord(mem[-1]))
    mem = mem[:-1]
    return True
  
  def clear_mem():
    global mem
    mem = ""
  
  def stack_to_mem():
    global mem

    while len(stacks[current_stack]) > 0:
      pop_to_mem()

  def mem_to_stack():
    global mem

    while len(mem) > 0:
      push_from_mem()
  
  def reverse_stack():
    stacks[current_stack].reverse()
  
  def reverse_mem():
    global mem
    mem = mem[::-1]
  
  def push_stack_len():
    global mem
    global stacks
    global current_stack

    stacks[current_stack].append(len(stacks[current_stack]))
  
  def push_mem_len():
    global mem
    global stacks
    global current_stack

    stacks[current_stack].append(len(mem))
  
  def pop_to_mem_str():
    global mem
    global stacks
    global current_stack

    val = stacks[current_stack].pop()
    val = str(val)

    mem += val

  cmds = {
    '00': discard,
    '01': duplicate,
    '02': rotate_top_2,
    '03': rotate_top_3,
    '04': clear_stack,
    '05': pop_to_mem,
    '06': push_from_mem,
    '07': clear_mem,
    '08': stack_to_mem,
    '09': mem_to_stack,
    '10': reverse_stack,
    '11': reverse_mem,
    '12': push_stack_len,
    '13': push_mem_len,
    '14': pop_to_mem_str,
  }

  cmd = cmds[value]
  cmd()

  return True

def stackcommands(value):
  global stacks
  global current_stack

  def switch_to(stack):
    global current_stack
    current_stack = stack
  
  def push_from(stack):
    global stacks
    global current_stack
    value = stacks[stack].pop()
    stacks[current_stack].append(value)
  
  def append_stack(stack):
    global stacks
    global current_stack

    stacks[current_stack].extend(stacks[stack])
  
  def replace_with(stack):
    global stacks
    global current_stack

    stacks[current_stack] = stacks[stack].copy()
  
  def clear_stack(stack):
    global stacks
    global current_stack

    stacks[current_stack] = []
  
  def stack_len(stack):
    global stacks
    global current_stack
    
    stacks[current_stack].append(len(stacks[stack]))

  cmds = {
    '0': switch_to,
    '1': push_from,
    '2': append_stack,
    '3': replace_with,
    '4': clear_stack,
    '5': stack_len,
  }

  cmdnum = value[0]
  stack = int(value[1])
  
  cmd = cmds[cmdnum]
  cmd(stack)

  return True
  

# Interpreter functions
def make_error(block, name, details):
  return f"\nError: {name}\n{details}\n{block}\n^ Here"

class Executor:
  def __init__(self, code):
    lines = code.split('\n')
    truelines = []
    for line in lines:
      if not line.startswith(';;'):
        truelines.append(line)
    prog = " ".join(truelines)
    blocks = re.split(' |\n', prog)

    # Error checking
    self.blocks = list(filter(lambda item: len(item) > 0, blocks))
    for block_ in self.blocks:
      if len(block_) != 3 and not block_.startswith(';'):
        error_ = make_error(
          block_,
          "Illegal Block Error",
          "Block of incorrect length",
        )
        return None, error_
    
    self.idx = -1
    self.block = ""
  
  def gotocommand(self, value):
    labelname = f"@{value}"
    try:
      label_idx = self.blocks.index(labelname)
      self.goto(label_idx - 1)
    except ValueError:
      print("Label", labelname, "not found.")
    
    return True
    
  def conditionalgoto(self, value):
    val = stacks[current_stack].pop()
    if val > 0:
      self.gotocommand(value)
    
    return True
  
  def get_command(self, identifier):
    def foo(value):
      return True

    commands = {
      '0': pushstack,
      '1': op,
      '2': io,
      '3': stackmemcommands,
      '4': stackcommands,
      '@': foo,
      '$': self.gotocommand,
      '?': self.conditionalgoto,
    }
    return commands.get(identifier, None)
  
  def goto(self, idx):
    self.idx = idx
    if idx < len(self.blocks):
      self.block = self.blocks[idx]
    else:
      self.block = None
    return self.block
  
  def advance(self):
    self.goto(self.idx + 1)
    return self.block

  def run(self):
    global stacks
    global current_stack
    global mem

    self.advance()
    while self.block is not None:
      identifier = self.block[0]
      if identifier == ';':
        self.advance()
        continue
      value = self.block[1:]
      cmd = self.get_command(identifier)
      if cmd is None:
        return None, make_error(
          self.block,
          "Illegal Command",
          "Identifier does not exist",
        )
      try:
        # prestack is for just in case the stack is too small to do an operation, but it only throws an indexerror after it has already popped one value from the stack, so it will restore the stack to what it was before.
        # print(mem)
        # print(stacks)
        prestack = stacks[current_stack].copy()
        result = cmd(value)
      except IndexError as e:
        raise e
        stacks[current_stack] = prestack.copy()
        return None, make_error(
          self.block,
          "Stack Error",
          "Stack is too small for operation",
        )
      if result is None:
        return None, make_error(
          self.block,
          "Illegal Command",
          "Command failed",
        )
      self.advance()

    return "", None
  

# with open("bigdata.sizzle") as f:
#   code = f.read()
# sizzle_exec = Executor(code)
# sizzle_exec.run()

tipsmsg = """
Sizzle Tips:
  To Run A File:
    1. Type 200 [Enter]
    2. Type (filename) [Enter]
    3. Type 207 [Enter]
    This gets your input with 200 and stores it in memory, and then runs the file in memory with 207.
  
  Useful Stuff:
    Run cv.s and type a string to get a list of the ascii codes for the string. This is useful because you cannot directly use strings in Sizzle.

    Run cvi.s and type a string to get the actual code you can copy into your file to add the string as ASCII values to the current stack. This is handy because typing out all of the ASCII codes (especially when using codes above 100) can get quite annoying.

    README.md has a full guide for everything you can do in the language. It doesn't hold your hand, but it is fairly simple to figure out.

    Because this is on replit, you cannot actually modify the files. That means that in order to run your own files, you have to either
      - Fork the repo
      OR
      - Copy and paste the file's contents into the shell. The shell behaves
        exactly like the file interpreter, so it will work the same. It will print annoying '> [line]' prompts in the middle of your output, but other than that there will be no difference.
"""

# while True:
#   with open('cvi.s', 'r') as f:
#     code = f.read()
#     se = Executor(code)
#     se.run()
#   break

# Shell
print("Welcome to the Sizzle shell. Check out README.md for instructions.")
print("Type 'tips' for some tips.")
while True:
  program = input("> ")

  if program.startswith(';;'): continue
  if program == "tips":
    print(tipsmsg)
    continue

  try:
    sizzle_exec = Executor(program)
    result, error = sizzle_exec.run()
    if error:
      print(error)
      continue
  except RecursionError as e:
    raise e
    print("o heck (recursion error)")
  
  print("")

# with open("truthmachine.sizzle") as f:
#   code = f.read()
# sizzle_exec = Executor(code)
# sizzle_exec.run()