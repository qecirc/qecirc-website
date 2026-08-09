OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[11];
s q[16];
s q[17];
s q[8];
cz q[12], q[6];
cz q[4], q[18];
cz q[2], q[3];
cz q[1], q[0];
cz q[13], q[7];
cz q[14], q[15];
cz q[19], q[5];
cz q[9], q[10];
