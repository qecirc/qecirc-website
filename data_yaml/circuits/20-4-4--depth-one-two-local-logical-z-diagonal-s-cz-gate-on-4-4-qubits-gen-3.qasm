OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[14];
s q[3];
s q[4];
s q[18];
s q[9];
s q[12];
cz q[10], q[8];
cz q[7], q[5];
cz q[2], q[11];
cz q[16], q[19];
cz q[1], q[0];
cz q[13], q[6];
cz q[15], q[17];
