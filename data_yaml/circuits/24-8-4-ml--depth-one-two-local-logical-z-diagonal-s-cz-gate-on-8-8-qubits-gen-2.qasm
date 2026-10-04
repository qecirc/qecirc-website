OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[3];
s q[15];
s q[2];
s q[14];
s q[1];
s q[13];
s q[7];
s q[9];
cz q[16], q[0];
cz q[8], q[23];
cz q[5], q[18];
cz q[4], q[6];
cz q[12], q[22];
cz q[11], q[21];
cz q[10], q[20];
cz q[17], q[19];
