OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[9];
s q[7];
s q[5];
s q[4];
s q[3];
s q[2];
s q[1];
s q[11];
s q[18];
s q[20];
s q[13];
s q[8];
s q[12];
s q[10];
id q[21];
cz q[9], q[12];
cz q[7], q[5];
cz q[4], q[10];
cz q[3], q[13];
cz q[2], q[1];
cz q[11], q[8];
cz q[18], q[20];
