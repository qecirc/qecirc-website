OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[12];
s q[9];
s q[5];
s q[4];
s q[3];
s q[2];
s q[1];
s q[13];
s q[10];
s q[20];
s q[15];
s q[11];
s q[6];
s q[18];
id q[14];
cz q[12], q[11];
cz q[9], q[1];
cz q[5], q[13];
cz q[4], q[2];
cz q[3], q[15];
cz q[10], q[6];
cz q[20], q[18];
