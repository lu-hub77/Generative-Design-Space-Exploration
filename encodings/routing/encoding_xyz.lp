%%%%%%%%%%%%%%%
%%  ROUTING  %%
%%%%%%%%%%%%%%%

%dimensional ordered rounting
coord(X,Y,Z) :- location((router,I),(X,Y,Z)).
next(X,Y,Z,X',Y',Z',X+1,Y,Z) :- coord(X,Y,Z), coord(X',Y',Z'), coord(X+1,Y,Z), X < X'.
next(X,Y,Z,X',Y',Z',X-1,Y,Z) :- coord(X,Y,Z), coord(X',Y',Z'), coord(X-1,Y,Z), X > X'.
next(X,Y,Z,X,Y',Z',X,Y+1,Z) :- coord(X,Y,Z), coord(X,Y',Z'), coord(X,Y+1,Z), Y < Y'.
next(X,Y,Z,X,Y',Z',X,Y-1,Z) :- coord(X,Y,Z), coord(X,Y',Z'), coord(X,Y-1,Z), Y > Y'.
next(X,Y,Z,X,Y,Z',X,Y,Z+1) :- coord(X,Y,Z), coord(X,Y,Z'), coord(X,Y,Z+1), Z < Z'.
next(X,Y,Z,X,Y,Z',X,Y,Z-1) :- coord(X,Y,Z), coord(X,Y,Z'), coord(X,Y,Z-1), Z > Z'.
reached(C,(link,LI),(TYPE,P),(router,R);C,(link,LI'),(router,R'),(TYPE',P')) :- bind(T,TYPE,P), bind(T',TYPE',P'), (TYPE,P)!=(TYPE',P'), send(T,C), read(T',C), 
						       location((TYPE,P),(X,Y,Z)), processingType(TYPE), location((router,R),(X,Y,Z)), connection((link,LI),(TYPE,P),(router,R)),
							   location((TYPE',P'),(X',Y',Z')), processingType(TYPE'), location((router,R'),(X',Y',Z')), connection((link,LI'),(router,R'),(TYPE',P')).
reached(C,(link,LI),(router,R),(router,R')) :- reached(C,_,_,(router,R)), location((router,R),(X,Y,Z)), location((router,R'),(X',Y',Z')),
					 read(T,C), bind(T,TTYPE,TP), location((TTYPE,TP),(TX,TY,TZ)), processingType(TTYPE),
					 next(X,Y,Z,TX,TY,TZ,X',Y',Z'), connection((link,LI),(router,R),(router,R')).
hops(C,N) :- bind(T1,TYPE,R), bind(T2,TYPE',R'), (TYPE,R)!=(TYPE',R'),
			 send(T1,C), read(T2,C), location((TYPE,R),(X,Y,Z)), processingType(TYPE), location((TYPE',R'),(X',Y',Z')), processingType(TYPE'),
			 N = |X-X'|+|Y-Y'|+|Z-Z'|+2.	
hops(C,0) :- bind(T1,TYPE,R), bind(T2,TYPE,R), send(T1,C), read(T2,C).	
