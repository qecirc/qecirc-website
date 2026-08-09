OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[10];
s q[3];
s q[19];
s q[16];
s q[17];
s q[9];
s q[13];
s q[11];
id q[14];
cz q[10], q[16];
cz q[3], q[9];
cz q[19], q[13];
cz q[17], q[11];
