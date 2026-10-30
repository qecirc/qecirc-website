OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[12];
s q[1];
s q[0];
s q[11];
s q[3];
s q[13];
s q[16];
s q[14];
s q[19];
s q[18];
s q[9];
s q[10];
id q[5];
cz q[12], q[10];
cz q[1], q[19];
cz q[0], q[13];
cz q[11], q[3];
cz q[16], q[14];
cz q[18], q[9];
