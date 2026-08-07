OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[8];
s q[7];
s q[5];
s q[3];
s q[21];
s q[13];
cz q[12], q[0];
cz q[6], q[10];
cz q[2], q[14];
cz q[1], q[4];
cz q[9], q[15];
cz q[23], q[18];
cz q[16], q[20];
cz q[22], q[17];
cz q[11], q[19];
