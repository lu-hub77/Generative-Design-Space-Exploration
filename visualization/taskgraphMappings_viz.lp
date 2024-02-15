% Get task graph elements
graph(taskgraph).
graph(A,taskgraph) :- application(A).
node(T,A) :- task(T,A).
node((map,T),A) :- task(T,A).
edge((T1,T2),A) :- comm(C,A), send(T1,C), read(T2,C).
edge((T,(map,T)),A) :- node(T,A), node((map,T),A).

% Node characteristics
attr(node,(map,T),label,(TYPE)) :- map(T,TYPE).
attr(node,(map,T),color,red) :- map(T,TYPE).

% Graph characteristics
attr(graph,taskgraph,label,"Application graph").
attr(graph,A,label,A) :- application(A).

% Edge characteristics
attr(edge,(T1,T2),label,C) :- comm(C,A), send(T1,C), read(T2,C).
attr(edge,(T1,T2),arrowhead,normal) :- comm(C,A), send(T1,C), read(T2,C).
attr(edge,(T,(map,T)),arrowhead,none) :- node(T,A), node((map,T),A).
attr(edge,(T,(map,T)),color,red) :- node(T,A), node((map,T),A).
attr(edge,(T,(map,T)),style,dashed) :- node(T,A), node((map,T),A).
