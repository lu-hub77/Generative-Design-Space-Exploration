% Get architecture graph elements
graph(architecture).
node((TYPE,I),architecture) :- allocated((TYPE,I)), processingType(TYPE).
node((TYPE,I),architecture) :- allocated((TYPE,I)), communicationType(TYPE).
edge((R1,R2),architecture) :- allocated((link,I)), connection((link,I),R1,R2).

% Graph characteristics
attr(graph,architecture,label,"Architecture graph").

% Node characteristics
attr(graph_nodes,architecture,style,filled).
attr(graph_nodes,architecture,width,1).
attr(graph_nodes,architecture,shape,square).

attr(node,(TYPE,I),fillcolor,gray) :- allocated((TYPE,I)), processingType(TYPE).
attr(node,(TYPE,I),fillcolor,white) :- allocated((TYPE,I)), communicationType(TYPE).
attr(node,(TYPE,I),label,(TYPE,I)) :- allocated((TYPE,I)), processingType(TYPE).
attr(node,(TYPE,I),label,(TYPE,I)) :- allocated((TYPE,I)), communicationType(TYPE).
attr(node,(TYPE,I),pos,@pos(X*4-1,Y*4+1)) :- location((TYPE,I),(X,Y,Z)), processingType(TYPE).
attr(node,(TYPE,I),pos,@pos(X*4+1,Y*4-1)) :- location((TYPE,I),(X,Y,Z)), communicationType(TYPE).

% Edge characteristics
attr(graph_edges,architecture,arrowType,vee).
attr(edge,(R1,R2),label,I) :- allocated((link,I)), connection((link,I),R1,R2).
