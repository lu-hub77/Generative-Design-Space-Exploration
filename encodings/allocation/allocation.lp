%%%%%%%%%%%%%%%%%
%% ALLOCATION  %%
%%%%%%%%%%%%%%%%%

allocated((TYPE,I)) :- bind(T,TYPE,I).

% Number of allocated processer instances depending on the lower and upper boundaries
% Allocate at least one and at maximum the number of available slots processing instances
:- { allocated((TYPE,_)) : processingType(TYPE) } L-1, generalLowerBound(L).
:- U+1 { allocated((TYPE,_)) : processingType(TYPE) }, generalUpperBound(U).
:- M+1 { allocated((TYPE,_)) : processingType(TYPE) }, numberProcessorSlots(M).
% Number per type
:- { allocated((TYPE,_)) } L-1, perTypeLowerBound(TYPE,L), processingType(TYPE).
:- U+1 { allocated((TYPE,_)) }, perTypeUpperBound(TYPE,U), processingType(TYPE). 

% Each allocated instance is also placed
:- not location((TYPE,NR),_), allocated((TYPE,NR)), processingType(TYPE).
% Each placed instance is also allocated
:- location((TYPE,NR),_), not allocated((TYPE,NR)), processingType(TYPE).

% Allocation of routers and links
allocated(R) :- reached(_,_,R,_). % communication instance 1
allocated(R) :- reached(_,_,_,R). % communication instance 2
allocated(R) :- reached(_,R,_,_). % interconnecting instance

% NOTE InstanceCount is defined to check solutions, but is not needed for experiments execution
% instanceCount(TYPE,N) :- N=#count{I:allocated((TYPE,I))}, processingType(TYPE).
% instanceCount(TYPE,N) :- N=#count{I:allocated((TYPE,I))}, communicationType(TYPE).
% instanceCount(TYPE,N) :- N=#count{I:allocated((TYPE,I))}, interconnectionType(TYPE).
