OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[12];
s q[10];
s q[7];
s q[0];
s q[17];
s q[6];
s q[18];
s q[13];
cz q[14], q[8];
cz q[5], q[15];
cz q[4], q[1];
cz q[3], q[9];
cz q[2], q[16];
cz q[19], q[11];
cz q[20], q[21];
