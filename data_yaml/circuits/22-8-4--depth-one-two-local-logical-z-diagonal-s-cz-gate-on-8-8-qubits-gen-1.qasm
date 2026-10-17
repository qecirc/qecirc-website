OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[1];
s q[12];
s q[9];
s q[18];
cz q[10], q[21];
cz q[6], q[11];
cz q[4], q[7];
cz q[3], q[15];
cz q[2], q[0];
cz q[8], q[16];
cz q[14], q[13];
cz q[5], q[20];
cz q[19], q[17];
