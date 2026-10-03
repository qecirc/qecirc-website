OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[8];
s q[3];
s q[2];
s q[1];
s q[5];
s q[0];
s q[9];
s q[10];
s q[15];
s q[17];
s q[18];
s q[19];
id q[16];
cz q[8], q[17];
cz q[3], q[15];
cz q[2], q[9];
cz q[1], q[10];
cz q[5], q[18];
cz q[0], q[19];
