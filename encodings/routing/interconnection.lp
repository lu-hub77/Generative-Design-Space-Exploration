%%%%%%%%%%%%%%%%%%%%%
%% INTERCONNECTION %%
%%%%%%%%%%%%%%%%%%%%%
% Interconnect each processing type instance with one router instance
1{ connection((link,LID),(TYPE,RID1),(router,RID2)) : LID=1..N }1 :- processingType(TYPE), location((TYPE,RID1),(X,Y,Z)), location((router,RID2),(X,Y,Z)), numberLinks(N).
% Build bi-directional interconenction
1{ connection((link,LID2),(router,RID2),(TYPE,RID1)) : LID2=1..N }1 :- connection((link,LID1),(TYPE,RID1),(router,RID2)), processingType(TYPE), numberLinks(N).

% Each connection has a unique identifier
:- connection((link,LID),(TYPE1,RID1),(TYPE2,RID2)), connection((link,LID),(TYPE1',RID1'),(TYPE2',RID2')), ((TYPE1,RID1),(TYPE2,RID2))!=((TYPE1',RID1'),(TYPE2',RID2')).

% Generation of an instance of the communicationType link
instance(link,LID) :- connection((link,LID),(TYPE1,RID1),(TYPE2,RID2)).
