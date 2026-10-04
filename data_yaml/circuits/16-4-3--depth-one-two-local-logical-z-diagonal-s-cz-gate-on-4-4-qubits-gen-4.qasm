OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[10];
s q[3];
s q[2];
s q[1];
s q[11];
s q[7];
s q[15];
s q[5];
s q[0];
s q[9];
s q[14];
s q[8];
id q[6];
cz q[10], q[8];
cz q[3], q[14];
cz q[2], q[0];
cz q[1], q[15];
cz q[11], q[7];
cz q[5], q[9];
