OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[2];
s q[11];
s q[3];
s q[16];
s q[14];
s q[17];
s q[15];
s q[8];
cz q[12], q[18];
cz q[6], q[4];
cz q[1], q[0];
cz q[13], q[19];
cz q[9], q[10];
cz q[7], q[5];
