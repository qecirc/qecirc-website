OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[8];
s q[4];
s q[2];
s q[12];
s q[0];
s q[11];
s q[5];
s q[10];
id q[20];
cz q[8], q[11];
cz q[4], q[0];
cz q[2], q[5];
cz q[12], q[10];
