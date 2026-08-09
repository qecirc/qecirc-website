OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[4];
s q[1];
s q[17];
s q[7];
s q[9];
s q[14];
s q[11];
s q[10];
cz q[12], q[13];
cz q[8], q[15];
cz q[6], q[16];
cz q[3], q[19];
cz q[2], q[0];
cz q[18], q[5];
