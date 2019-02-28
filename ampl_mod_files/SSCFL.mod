set facility;
set client;
param C{client,facility};
param F{facility};
param W{client};
param Q{facility};
var x{client,facility} binary;
var y{facility} binary;
minimize f: sum{i in client, j in facility}C[i,j]*x[i,j] +
			sum{j in facility}F[j]*y[j];
s.t. v1{i in client}:sum{j in facility}x[i,j] = 1;
s.t. v2{j in facility}:sum{i in client}W[i]*x[i,j]<=Q[j]*y[j];