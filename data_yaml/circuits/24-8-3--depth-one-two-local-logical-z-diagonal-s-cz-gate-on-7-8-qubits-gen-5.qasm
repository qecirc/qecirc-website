OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[16];
s q[12];
s q[20];
s q[8];
s q[6];
s q[10];
s q[4];
s q[3];
s q[5];
s q[19];
s q[15];
s q[23];
id q[9];
cz q[16], q[8];
cz q[12], q[6];
cz q[20], q[10];
cz q[4], q[15];
cz q[3], q[19];
cz q[5], q[23];
