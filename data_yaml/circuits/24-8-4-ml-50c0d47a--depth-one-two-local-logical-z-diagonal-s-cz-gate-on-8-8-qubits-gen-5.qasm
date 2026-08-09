OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[3];
s q[14];
s q[12];
s q[9];
cz q[16], q[21];
cz q[10], q[8];
cz q[6], q[4];
cz q[2], q[0];
cz q[1], q[13];
cz q[7], q[5];
cz q[23], q[19];
cz q[22], q[17];
cz q[15], q[11];
cz q[18], q[20];
