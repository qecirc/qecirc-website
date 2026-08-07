OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[16];
s q[12];
s q[20];
s q[8];
s q[6];
s q[10];
s q[1];
s q[0];
s q[2];
s q[18];
s q[14];
s q[22];
cz q[4], q[13];
cz q[3], q[17];
cz q[5], q[21];
cz q[19], q[9];
cz q[15], q[7];
cz q[23], q[11];
