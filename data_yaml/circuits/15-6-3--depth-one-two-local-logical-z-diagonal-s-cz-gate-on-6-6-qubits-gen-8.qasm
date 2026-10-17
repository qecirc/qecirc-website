OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[8];
s q[2];
s q[1];
s q[0];
s q[12];
s q[6];
s q[13];
s q[3];
s q[11];
s q[10];
s q[5];
s q[14];
id q[9];
cz q[8], q[6];
cz q[2], q[14];
cz q[1], q[11];
cz q[0], q[3];
cz q[12], q[13];
cz q[10], q[5];
