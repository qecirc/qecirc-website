OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[0];
s q[12];
s q[1];
s q[6];
s q[8];
s q[3];
s q[14];
s q[10];
cz q[2], q[11];
cz q[13], q[9];
cz q[15], q[7];
cz q[5], q[4];
