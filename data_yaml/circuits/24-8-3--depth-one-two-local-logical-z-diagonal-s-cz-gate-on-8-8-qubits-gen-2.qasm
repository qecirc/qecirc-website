OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[6];
s q[1];
s q[15];
s q[13];
cz q[16], q[5];
cz q[12], q[4];
cz q[20], q[3];
cz q[8], q[10];
cz q[0], q[2];
cz q[19], q[23];
cz q[18], q[11];
cz q[14], q[7];
cz q[22], q[9];
cz q[21], q[17];
