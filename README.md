## lineafier
Automatically converts any python script to a one liner so you don't have to!

## Notes
Does not check if the syntax is valid, if it isn't it may cause errors.

## Drawbacks
- The variables _, , _return_value, _return, _continue, _break,  are used, and code that make use of them may not function correctly
- Does not convert comments or type hints
- Match is implemented as an if-else chain
- Functions are replaced by lambda functions
- The builtin "sum" function is used, so it must not be overridden