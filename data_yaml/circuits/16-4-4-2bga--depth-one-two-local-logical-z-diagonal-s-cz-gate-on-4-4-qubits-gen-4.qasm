OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[4];
s q[2];
s q[0];
s q[12];
s q[10];
s q[9];
s q[5];
cz q[6], q[1];
cz q[14], q[11];
cz q[3], q[7];
cz q[13], q[15];
