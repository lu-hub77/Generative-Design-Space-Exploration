%%%%%%%%%%%%%%%%%%%%%%%%
%%  Problem Encoding  %%
%%%%%%%%%%%%%%%%%%%%%%%%

% At maximum each task is mapped to one own instance of that type
upperBound(TYPE,N) :- numberMappings(TYPE,N).

% NOTE Version one: One instance is necessary if there is one task with only one mapping option to this processing typ
lowerBound(TYPE,1) :- options(T,1), map(T,TYPE).
lowerBound(TYPE,0) :- processingType(TYPE), not lowerBound(TYPE,1).

% NOTE Version two: Assume two tasks have the same only one option to be bind on (type binding) AND the sum of execution times of both is greater than the period of the application, then at least two instances of the specific type are required.
% Lower bound is adapted accordingly.
% TODO Is not completely correct yet, e.g. consider 120/60 = 2 -> 2 or 3 instances?
% lowerBoundHelper(TYPE,N+1) :- processingType(TYPE), Time1=#sum{E,T:executionTime((T,TYPE),E), options(T,1), map(T,TYPE)}, period(Time2), N=Time1/Time2.
% lowerBound(TYPE,N) :- N=#max{X : lowerBoundHelper(TYPE,X)}, processingType(TYPE), options(T,1), map(T,TYPE).
% lowerBound(TYPE,0) :- N=#count{T: options(T,1), map(T,TYPE)}, processingType(TYPE), N=0.
