# N-Queens CSP

## Setup and Running
To download and setup pypy3 if you dont already have it on your system (Linux and Mac):
```
$ sudo ./setup.sh
```

To run the program (Linux):
```
$ pypy3.3 Python3/main.py N [-v] [-a]
```

- N: the number of queens on the board
- -v: print out the solved board to the console if N is a large number
- -a: print out the inital and solved board to the console

Examples:
```
$ pypy3.3 Python3/main.py 1000
$ pypy3.3 Python3/main.py 100 -v
$ pypy3.3 Python3/main.py 10000 -a
```

To run the program (Mac):
```
$ pypy3 Python3/main.py N [-v] [-a]
```

---

## Updates
Update 1 [Razi][Razi]: I did most of the program in Java. But it doesn't actually spit out the right answer.
The program properly calculated the number of conflicts in each row of its column.
But when it's current position's conflicts are the same as the other position's conflicts it stays the same.And doesn't switch.
I'll try to add some comments later. Convert it Python, if you can. I'll convert it later, if I have time. Feel free to change it up.

Update 2 [Theodore][Theodore]: Got the program working in Python. It has a version of Tabu search implemented but I think it's a very hacky solution so it'll have to fixed up later.
There is also a Greedy Search Algorithm that palces the queens on the board to improve the time it takes to solve the problem.
I also removed the Java folder since we have decided to focus on optimizing/improving the python version of the code for now. We can re-try to do the code in Java once we finish with the Python code.


Update 3 [Theodore][Theodore]:
- Changed variables: [Q1,Q2,...,QN] -> [1,2,...,N]
- Changed domains: {Q1:[1,#],...,QN:[N,#]} -> {1:#,...,N:#}

Update 4:
- Use [pypy3][PyPy] to run the program instead of python3 because it improves the runtime of the program
- ```$ pypy3.3 main.py 1000``` instead of ```$ python3 main.py 1000```

Update 5:
- added ```setup.sh``` file to setup environment easily

Update 6:
- added the board object
- colour for the queens on the output
- comments and updated the setup.sh file


<!-- links -->
[Razi]:     https://github.com/RaziAbbasi
[Theodore]: https://github.com/th30retical
[PyPy]:     http://pypy.org/
