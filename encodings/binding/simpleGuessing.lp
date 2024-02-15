% This encoding is simply guessing the bound task and the processing type at every position in a grid

% Allowed positions in the grid
implicitPosition(NR,(X,Y,Z)) :- dimension(NX,NY,NZ), X=1..NX, Y=1..NY, Z=1..NZ, NR=X+NX*(Y-1)+NX*NY*(Z-1).

% Guessing of task binding and processing type per position
1 { placeBind(T,NR) : implicitPosition(NR,_) } 1 :- task(T).
{ placeType(TYPE,NR) : processingType(TYPE) } 1 :- implicitPosition(NR,_).
location((TYPE,NR),(X,Y,Z)) :- placeBind(T,NR), placeType(TYPE,NR), implicitPosition(NR,(X,Y,Z)).
bind(T,TYPE,NR) :- placeBind(T,NR), placeType(TYPE,NR).

% Task is bound exactely once and the processing type must fit at the respective position
:- placeBind(T,NR), placeType(TYPE,NR), not map(T,TYPE).

% No binding without a respective location and no location without a respective binding 
:- placeBind(_,NR), not placeType(_,NR).
:- placeType(_,NR), not placeBind(_,NR).
