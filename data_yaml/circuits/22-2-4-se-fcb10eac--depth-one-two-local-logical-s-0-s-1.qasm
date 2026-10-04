OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[6];
s q[3];
s q[2];
s q[1];
s q[21];
s q[18];
s q[15];
s q[16];
cz q[14], q[4];
cz q[10], q[20];
cz q[8], q[5];
cz q[0], q[11];
cz q[7], q[13];
cz q[19], q[9];
cz q[12], q[17];
