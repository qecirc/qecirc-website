OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[10];
s q[6];
s q[9];
s q[11];
cz q[3], q[4];
cz q[2], q[15];
cz q[14], q[5];
cz q[12], q[8];
cz q[1], q[0];
cz q[13], q[7];
