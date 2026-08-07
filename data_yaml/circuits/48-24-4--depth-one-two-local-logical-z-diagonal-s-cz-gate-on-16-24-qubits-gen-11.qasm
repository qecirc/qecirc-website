OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[9];
s q[5];
s q[36];
s q[20];
s q[35];
s q[19];
s q[34];
s q[18];
s q[33];
s q[17];
s q[42];
s q[46];
id q[47];
cz q[9], q[5];
cz q[36], q[20];
cz q[35], q[19];
cz q[34], q[18];
cz q[33], q[17];
cz q[42], q[46];
