#!/usr/bin/env python
# This is a one-off program to pull the BNF rules, by "production number",
# from ##DRIVER.xpl.  The result is embedded into runtimeC.c and g.py source
# code, rather than having any use of its own.  But here it is, if you want it.

import sys

rules = {}

for line in sys.stdin:
    if not line.startswith(" /*    ") or line[70:72] != "*/":
        continue
    lineNumber = int(line[7:10].strip())
    rule = " ".join(line[13:70].strip().split())
    
    if lineNumber not in rules:
        if rule.startswith("|"):
            fields = rules[lineNumber-1].split("::=")
            rule = fields[0] + "::= " + rule[2:]
        rules[lineNumber] = rule
    else:
        rules[lineNumber] += " " + rule

for n in rules:
    print(f"\"->->->->->->PRODUCTION NUMBER {n}: {rules[n]}\",")