OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[12];
s q[11];
s q[4];
s q[5];
cz q[10], q[14];
cz q[6], q[8];
cz q[3], q[9];
cz q[2], q[1];
cz q[0], q[7];
cz q[13], q[15];
