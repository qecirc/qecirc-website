OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[8];
s q[6];
s q[16];
s q[3];
s q[10];
s q[11];
cz q[5], q[17];
cz q[4], q[13];
cz q[2], q[12];
cz q[1], q[7];
cz q[0], q[14];
cz q[15], q[9];
