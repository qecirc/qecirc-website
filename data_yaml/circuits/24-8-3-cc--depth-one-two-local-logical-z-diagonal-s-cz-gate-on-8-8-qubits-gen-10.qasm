OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[12];
s q[22];
s q[16];
s q[18];
s q[10];
s q[20];
s q[13];
s q[23];
s q[15];
s q[17];
s q[11];
s q[21];
cz q[14], q[1];
cz q[9], q[0];
cz q[19], q[2];
cz q[7], q[4];
cz q[6], q[3];
cz q[8], q[5];
