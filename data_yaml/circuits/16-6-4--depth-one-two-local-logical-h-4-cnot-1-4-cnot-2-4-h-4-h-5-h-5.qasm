OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[2];
s q[6];
s q[10];
s q[15];
s q[3];
s q[7];
s q[11];
s q[14];
cz q[2], q[7];
cz q[6], q[3];
cz q[10], q[15];
cz q[11], q[14];
