OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[12];
s q[10];
s q[9];
cz q[6], q[11];
cz q[4], q[5];
cz q[14], q[3];
cz q[2], q[0];
cz q[1], q[15];
cz q[13], q[7];
