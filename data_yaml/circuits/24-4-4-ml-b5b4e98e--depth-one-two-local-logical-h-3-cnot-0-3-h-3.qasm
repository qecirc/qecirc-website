OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[10];
s q[8];
s q[5];
s q[4];
s q[3];
s q[17];
s q[13];
s q[12];
id q[14];
cz q[10], q[4];
cz q[8], q[17];
cz q[5], q[13];
cz q[3], q[12];
