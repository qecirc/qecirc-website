OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

s q[8];
s q[4];
s q[2];
s q[1];
s q[12];
s q[13];
s q[7];
s q[10];
id q[9];
cz q[8], q[13];
cz q[4], q[2];
cz q[1], q[7];
cz q[12], q[10];
