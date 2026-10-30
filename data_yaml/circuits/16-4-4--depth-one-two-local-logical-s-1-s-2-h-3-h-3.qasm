OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[10];
s q[6];
s q[3];
s q[14];
s q[12];
s q[1];
s q[9];
s q[11];
s q[0];
s q[4];
s q[7];
s q[5];
id q[8];
cz q[10], q[0];
cz q[6], q[3];
cz q[14], q[5];
cz q[12], q[7];
cz q[1], q[9];
cz q[11], q[4];
