OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[14];
s q[7];
s q[5];
s q[13];
s q[4];
s q[6];
s q[18];
s q[9];
cz q[10], q[19];
cz q[3], q[12];
cz q[2], q[11];
cz q[16], q[8];
cz q[1], q[15];
cz q[0], q[17];
