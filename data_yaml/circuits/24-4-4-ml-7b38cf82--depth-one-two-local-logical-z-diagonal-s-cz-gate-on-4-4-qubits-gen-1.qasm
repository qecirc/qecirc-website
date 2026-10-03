OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[5];
s q[4];
s q[19];
s q[17];
cz q[16], q[20];
cz q[10], q[2];
cz q[8], q[12];
cz q[6], q[14];
cz q[3], q[7];
cz q[1], q[13];
cz q[15], q[11];
cz q[0], q[9];
cz q[18], q[21];
cz q[23], q[22];
