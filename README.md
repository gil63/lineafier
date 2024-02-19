## lineafier
Automatically converts any python script to a one liner so you don't have to!

## Drawbacks
- The variable _ is overridden on every for/while loop iteration start
- Does not convert comments or type hints
- Match is implemented as an if-else chain
- Functions are replaced by lambda functions
- The builtin "sum" function is used, so it must not be overridden