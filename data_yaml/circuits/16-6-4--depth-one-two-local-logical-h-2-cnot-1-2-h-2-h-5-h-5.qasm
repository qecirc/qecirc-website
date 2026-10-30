OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[8];
s q[4];
s q[1];
s q[0];
s q[5];
s q[9];
s q[12];
s q[13];
id q[14];
cz q[8], q[0];
cz q[4], q[12];
cz q[1], q[9];
cz q[5], q[13];
