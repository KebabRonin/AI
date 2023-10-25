```py
state = ([8, 6, 7, 2, 5, 4, 0, 3, 1], None)
```

Modelul ales contine un vector de n elemente care retine pozitiile pieselor
si inca un numar, care reprezinta ultima directie in care am mutat '0'.

La fiecare pas, pot alege dintre maxim 3 directii de mutat, NESW,
din care scot ultima piesa mutata.

Cum pentru a avea pozitia goala, trebuie sa fi mutat '0' in directia opusa
pasului precedent (UP - DOWN/ LEFT - RIGHT), inseamna ca toate directiile
care nu ies din matrice sunt valide, exceptand opusul directiei ultimei miscari.

Ex:
```py
 0  1  2  3  4  5  6  7  8
[8, 6, 7, 2, 5, 4, 0, 3, 1]  |  last_move = None / UP / RIGHT / DOWN / LEFT

 8  6  7
 2  5  4
 0  3  1

Mutari valide: [UP, RIGHT]

Aleg UP

 0  1  2  3  4  5  6  7  8
[8, 6, 7, 0, 5, 4, 2, 3, 1]  |  last_move = UP

 8  6  7
 0  5  4
 2  3  1

Mutari valide: [UP, RIGHT] = [UP, RIGHT, DOWN] - (DOWN)
```

###Rezultate Rulare algoritmi
```
======================IDDFS=======================
([2, 5, 3, 1, 0, 6, 4, 7, 8], None) --4 steps (0.000997304916381836s) --> ['UP', 'LEFT', 'DOWN', 'DOWN']

([2, 7, 5, 0, 8, 4, 3, 1, 6], None) --21 steps (3.7897756099700928s) --> ['UP', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'UP']

([8, 6, 7, 2, 5, 4, 0, 3, 1], None) --28 steps (250.81653785705566s) --> ['UP', 'UP', 'RIGHT', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'UP']

==============greedy with manhattan===============
([2, 5, 3, 1, 0, 6, 4, 7, 8], None) --4 steps (0.0s) --> ['UP', 'LEFT', 'DOWN', 'DOWN']

([2, 7, 5, 0, 8, 4, 3, 1, 6], None) --21 steps (12.639405012130737s) --> ['UP', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'UP']

([8, 6, 7, 2, 5, 4, 0, 3, 1], None) --28 steps (308.9513986110687s) --> ['RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'UP']

===============greedy with hamming================
([2, 5, 3, 1, 0, 6, 4, 7, 8], None) --4 steps (0.0s) --> ['UP', 'LEFT', 'DOWN', 'DOWN']

([2, 7, 5, 0, 8, 4, 3, 1, 6], None) --21 steps (10.5875244140625s) --> ['UP', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'UP']

([8, 6, 7, 2, 5, 4, 0, 3, 1], None) --28 steps (301.66232895851135s) --> ['UP', 'UP', 'RIGHT', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'UP']
```