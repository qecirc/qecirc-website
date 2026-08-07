OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[8];
s q[4];
s q[2];
s q[0];
s q[12];
s q[10];
s q[14];
s q[6];
id q[5];
cz q[8], q[6];
cz q[4], q[10];
cz q[2], q[12];
cz q[0], q[14];
