OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[10];
s q[6];
s q[41];
s q[24];
s q[40];
s q[23];
s q[39];
s q[22];
s q[38];
s q[21];
s q[37];
s q[45];
id q[47];
cz q[10], q[6];
cz q[41], q[24];
cz q[40], q[23];
cz q[39], q[22];
cz q[38], q[21];
cz q[37], q[45];
