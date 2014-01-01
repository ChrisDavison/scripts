# Introduction

Go from formatted braille to english or vice-versa.

Formatted braille uses:

'O' - Raised portion
'.' - Lower portion

# Usage

braille -f braillefile.txt

braille -m message

## Hello World

Input of the text file *helloworld.txt*

```
O. O. O. O. O. .O O. O. O. OO
OO .O O. O. .O OO .O OO O. .O
.. .. O. O. O. .O O. O. O. ..
```

using command

```
braille -f helloworld.txt
```

results in
```
helloworld
```