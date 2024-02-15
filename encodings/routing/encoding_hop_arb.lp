%%%%%%%%%%%%%%%
%%  ROUTING  %%
%%%%%%%%%%%%%%%

node(N;N') :- connection((link,_),N,N').
nr_links(NR) :- NR=#count{ connection((link,I),N,N') : connection((link,I),N,N'), connection((link,I),N',N), N<N'; connection((link,I),N,N') : connection((link,I),N,N'), not connection((link,I),N',N) }.

{ reached(C,(link,I),N,N') : connection((link,I),N,N') } 1 :- node(N), comm(C,A).
{ reached(C,(link,I),N,N') : connection((link,I),N,N') } 1 :- node(N'), comm(C,A).

visit(C,(TYPE,I)) :- send(T,C), bind(T,TYPE,I).
visit(C,R') :- visit(C,R), reached(C,_,R,R').
:- reached(C,_,_,R), not visit(C,R).
:- reached(C,_,R,_), not visit(C,R).
:- read(T,C), bind(T,TYPE,I), not visit(C,(TYPE,I)).
:- read(T,C), bind(T,TYPE,I), reached(C,_,(TYPE,I),_).
	
hops(C,(TYPE,I),0)    :- send(T,C), bind(T,TYPE,I).
hops(C,R',H+1) :- hops(C,R,H), reached(C,_,R,R'), H<NR, nr_links(NR).
hops(C,H)      :- hops(C,(TYPE,I),H), read(T',C), bind(T',TYPE,I).	
