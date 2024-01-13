<h1>lineafier</h1>
Automatically converts any python script to a one liner so you don't have to!

<h3>Drawbacks</h3>
1. The variable _ is overridden on every for/while loop iteration start.
2. Does not convert comments or type hints
3. Match is implemented as an if-else chain
4. Functions are replaced by lambda functions
5. The builtin "sum" function is used, so it must not be overridden