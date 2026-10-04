OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[2];
s q[1];
s q[0];
s q[3];
s q[12];
s q[11];
s q[10];
s q[13];
id q[15];
cz q[2], q[11];
cz q[1], q[12];
cz q[0], q[13];
cz q[3], q[10];
