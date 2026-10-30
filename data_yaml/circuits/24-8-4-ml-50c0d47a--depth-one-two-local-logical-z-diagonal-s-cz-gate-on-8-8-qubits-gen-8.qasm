OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[10];
s q[1];
s q[8];
s q[23];
s q[22];
s q[15];
s q[14];
s q[12];
s q[11];
s q[13];
s q[17];
s q[19];
cz q[16], q[0];
cz q[6], q[3];
cz q[4], q[9];
cz q[2], q[20];
cz q[7], q[18];
cz q[5], q[21];
