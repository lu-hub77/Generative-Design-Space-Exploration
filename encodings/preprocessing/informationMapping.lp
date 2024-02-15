%% This programm analyzes extra information on the mapping options

% Number of mapping options per type
numberMappings(TYPE,N) :- processingType(TYPE), N=#count{T:map(T,TYPE)}.
% Number of mapping options per task
options(T,N) :- task(T,A), N=#count{TYPE:map(T,TYPE)}.
% Information, which tasks are mappped to the same processing types
shareMapping(T1,T2) :- map(T1,TYPE), map(T2,TYPE), T1<T2.
