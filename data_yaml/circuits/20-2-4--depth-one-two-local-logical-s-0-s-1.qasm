OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[14];
s q[10];
s q[3];
s q[1];
s q[0];
s q[12];
s q[7];
s q[15];
cz q[6], q[2];
cz q[5], q[19];
cz q[4], q[8];
cz q[9], q[18];
cz q[11], q[17];
cz q[13], q[16];
