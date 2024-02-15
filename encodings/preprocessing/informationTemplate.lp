%% This programm contains and analyzes extra information on the hardware template

% Dimension of the grid template
dimension(X,Y,Z) :- X=#max {N : location((router,_),(N,_,_))}, Y=#max {N : location((router,_),(_,N,_))}, Z=#max {N : location((router,_),(_,_,N))}.  

% Number of maximal available slots for placing processing instances
numberProcessorSlots(N) :- dimension(NX,NY,NZ), N=NX*NY*NZ.
