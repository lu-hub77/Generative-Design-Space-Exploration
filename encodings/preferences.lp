_preference(latency,max).
_preference(latency,(1,1,(T,TYPE,I,Time)),1,for(atom(bind(T,TYPE,I))),(T,Time,bind(T,TYPE,I))) :- map(T,TYPE), executionTime((T,TYPE),Time), task(T), I=1..X*Y*Z, dimension(X,Y,Z).
_holds(atom(bind(T,TYPE,I)),0) :- bind(T,TYPE,I), map(T,TYPE), executionTime((T,TYPE),Time).

_preference(energy,sum).
_preference(energy,(2,1,(P,TYPE,I,T)),1,for(atom(bind(T,TYPE,I))),(P,bind(T,TYPE,I))) :- map(T,TYPE), dynamicEnergy((T,TYPE),P), task(T), I=1..X*Y*Z, dimension(X,Y,Z).
_holds(atom(bind(T,TYPE,I)),0) :- bind(T,TYPE,I), map(T,TYPE), dynamicEnergy((T,TYPE),P).
_preference(energy,(2,2,(P,TYPE,I)),1,for(atom(allocated((TYPE,I)))),(P,allocated((TYPE,I)))) :- staticPower(TYPE,P), I=1..X*Y*Z, dimension(X,Y,Z).
_holds(atom(allocated((TYPE,I))),0) :- allocated((TYPE,I)), staticPower(TYPE,P).
% NOTE transmissionEnergy(link,P) is here fixed to interconnectionType link, for more types there is a differentiation required
_preference(energy,(2,3,(P,C,L)),1,for(atom(reached(C,L))),(P,reached(C,L))) :- connectedLocation(L,POSITION1,POSITION2), comm(C,A), transmissionEnergy(link,P).
_holds(atom(reached(C,L,R1,R2)),0) :- reached(C,L,R1,R2).

_preference(cost,sum).
_preference(cost,(3,1,(C,TYPE,I)),1,for(atom(allocated((TYPE,I)))),(C,allocated((TYPE,I)))) :- resourceCost(TYPE,C), I=1..X*Y*Z, dimension(X,Y,Z).
_holds(atom(allocated((TYPE,I))),0) :- allocated((TYPE,I)), resourceCost(TYPE,C).
