OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[12];
s q[10];
s q[3];
s q[41];
s q[2];
s q[40];
s q[1];
s q[39];
s q[0];
s q[38];
s q[11];
s q[37];
id q[47];
cz q[12], q[10];
cz q[3], q[41];
cz q[2], q[40];
cz q[1], q[39];
cz q[0], q[38];
cz q[11], q[37];
