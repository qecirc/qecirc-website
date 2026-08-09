OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[5];
s q[1];
s q[8];
s q[9];
cz q[10], q[0];
cz q[6], q[12];
cz q[3], q[7];
cz q[2], q[11];
cz q[4], q[14];
cz q[15], q[13];
