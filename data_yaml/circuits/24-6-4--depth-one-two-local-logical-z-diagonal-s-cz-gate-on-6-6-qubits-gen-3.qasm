OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[2];
s q[4];
s q[16];
s q[10];
s q[11];
s q[17];
cz q[12], q[8];
cz q[7], q[15];
cz q[6], q[20];
cz q[5], q[18];
cz q[3], q[0];
cz q[1], q[19];
cz q[9], q[21];
cz q[23], q[13];
cz q[22], q[14];
