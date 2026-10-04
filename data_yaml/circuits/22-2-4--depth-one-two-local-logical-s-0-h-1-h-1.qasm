OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[10];
s q[3];
s q[2];
s q[1];
s q[20];
s q[0];
s q[21];
s q[15];
s q[12];
s q[16];
s q[11];
s q[13];
id q[19];
cz q[10], q[11];
cz q[3], q[15];
cz q[2], q[16];
cz q[1], q[0];
cz q[20], q[12];
cz q[21], q[13];
