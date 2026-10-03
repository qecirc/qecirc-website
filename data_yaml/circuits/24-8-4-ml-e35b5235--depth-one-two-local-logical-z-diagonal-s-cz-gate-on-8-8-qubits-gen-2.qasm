OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[19];
s q[17];
s q[18];
s q[16];
cz q[12], q[20];
cz q[10], q[1];
cz q[8], q[2];
cz q[6], q[7];
cz q[4], q[5];
cz q[23], q[13];
cz q[21], q[14];
cz q[0], q[9];
cz q[22], q[15];
cz q[3], q[11];
