OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[18];
s q[8];
s q[5];
s q[4];
s q[20];
s q[21];
s q[9];
s q[19];
cz q[10], q[7];
cz q[6], q[3];
cz q[2], q[15];
cz q[1], q[11];
cz q[0], q[17];
cz q[12], q[16];
cz q[14], q[13];
