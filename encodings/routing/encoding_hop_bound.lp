%%%%%%%%%%%%%%%
%%  ROUTING  %%
%%%%%%%%%%%%%%%

node(N;N') :- connection((link,_),N,N').
{ reached(C,(link,I),N,N') : connection((link,I),N,N') } 1 :- node(N), comm(C,A).
{ reached(C,(link,I),N,N') : connection((link,I),N,N') } 1 :- node(N'), comm(C,A).

visit(C,(TYPE,I)) :- send(T,C), bind(T,TYPE,I).
visit(C,R') :- visit(C,R), reached(C,_,R,R').
:- reached(C,_,_,R), not visit(C,R).
:- reached(C,_,R,_), not visit(C,R).
:- read(T,C), bind(T,TYPE,I), not visit(C,(TYPE,I)).
:- read(T,C), bind(T,TYPE,I), reached(C,_,(TYPE,I),_).

% ensure all routes have smallest number of hops (same as dimensional ordered routing)
hops(C,N) :- bind(T1,TYPE,I), bind(T2,TYPE',I'), (TYPE,I)!=(TYPE',I'),
			 send(T1,C), read(T2,C),
			 location((TYPE,I),(X,Y,Z)), location((TYPE',I'),(X',Y',Z')),
			 N = |X-X'|+|Y-Y'|+|Z-Z'|+2.	
hops(C,0) :- bind(T1,TYPE,I), bind(T2,TYPE,I),
						send(T1,C), read(T2,C).	
:- hops(C,N), not N { reached(C,L,_,_) : reached(C,L,_,_) } N.
