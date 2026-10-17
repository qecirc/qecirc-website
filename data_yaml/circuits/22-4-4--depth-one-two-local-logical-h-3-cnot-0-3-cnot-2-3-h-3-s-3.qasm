OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[8];
s q[6];
s q[4];
s q[2];
s q[12];
s q[1];
s q[0];
s q[13];
s q[11];
s q[9];
s q[5];
s q[10];
id q[20];
cz q[8], q[5];
cz q[6], q[13];
cz q[4], q[2];
cz q[12], q[0];
cz q[1], q[9];
cz q[11], q[10];
