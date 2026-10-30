OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[7];
s q[5];
s q[3];
s q[2];
s q[11];
s q[9];
s q[10];
s q[4];
id q[15];
cz q[7], q[2];
cz q[5], q[11];
cz q[3], q[9];
cz q[10], q[4];
