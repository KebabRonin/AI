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