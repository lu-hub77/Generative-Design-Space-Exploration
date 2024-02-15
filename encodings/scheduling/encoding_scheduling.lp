%%%%%%%%%%%%%%%%%%
%%  SCHEDULING  %%
%%%%%%%%%%%%%%%%%%

%all starting times are bigger than 0
%T>=0 --> -T<=0 --> 0-T<=0
&diff { 0-T } <= 0 :- task(T).

%all tasks have to finish before their deadline
%T<=DL-e(T) --> T-0<=DL-e(T)
&diff { T-0 } <= V :- period(P), bind(T,TYPE,I), executionTime((T,TYPE),Time), V=P-Time.


%tasks bound onto the same resource have to be scheduled successively   
%T2-T1>=ET_T1 --> -T2+T1<=-ET_T1 --> T1-T2<=-ET_T1
&diff { T1-T2 } <= -Time1 :- task(T1), task(T2), T1<T2,
							                   bind(T1,TYPE,I), bind(T2,TYPE,I),
							                   priority(T1,T2),
							                   executionTime((T1,TYPE),Time1).
&diff { T2-T1 } <= -Time2 :- task(T1), task(T2), T1<T2,
							                   bind(T1,TYPE,I), bind(T2,TYPE,I),
							                   not priority(T1,T2),
                                               not depends_trans(T1,T2), 
											   not depends_trans(T2,T1),
							                   executionTime((T2,TYPE),Time2).
	
	

%communication scheduling
%Start hop
&diff { T1-C } <= -Time :- send(T1,C),
					       bind(T1,TYPE,I),
                           executionTime((T1,TYPE),Time).

%Middle hops			
&diff { C1-C2 } <= -S :- conflict(C1,C2), priority(C1,C2), 
                         hops(C1,N), transmissionDelay(link,D), S=N*D.
&diff { C2-C1 } <= -S :- conflict(C1,C2), not priority(C1,C2), 
                         hops(C2,N), transmissionDelay(link,D), S=N*D.

%Last hop
&diff { C-T } <= -S :- read(T,C), hops(C,N), transmissionDelay(link,D), S=N*D.

#show hops/2.
