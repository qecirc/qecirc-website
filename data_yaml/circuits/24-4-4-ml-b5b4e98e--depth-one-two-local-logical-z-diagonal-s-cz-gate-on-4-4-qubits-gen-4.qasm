OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[20];
s q[5];
s q[17];
s q[1];
s q[0];
s q[18];
s q[7];
s q[23];
s q[15];
s q[22];
s q[21];
s q[11];
cz q[10], q[9];
cz q[8], q[2];
cz q[6], q[14];
cz q[4], q[12];
cz q[3], q[16];
cz q[19], q[13];
