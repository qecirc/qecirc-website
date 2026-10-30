OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[12];
s q[6];
s q[5];
s q[3];
s q[9];
s q[14];
s q[10];
s q[13];
s q[21];
s q[18];
s q[23];
s q[20];
id q[22];
cz q[12], q[5];
cz q[6], q[18];
cz q[3], q[21];
cz q[9], q[14];
cz q[10], q[23];
cz q[13], q[20];
