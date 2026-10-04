OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[16], q[8];
cz q[7], q[31];
cz q[6], q[29];
cz q[30], q[5];
cz q[23], q[14];
cz q[15], q[22];
cz q[4], q[28];
cz q[21], q[13];
cz q[3], q[27];
cz q[20], q[12];
cz q[2], q[24];
cz q[26], q[0];
cz q[19], q[9];
cz q[11], q[17];
cz q[1], q[25];
cz q[18], q[10];
