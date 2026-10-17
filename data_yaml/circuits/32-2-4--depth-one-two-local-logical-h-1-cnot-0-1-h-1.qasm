OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[28], q[24];
cz q[25], q[27];
cz q[22], q[31];
cz q[20], q[30];
cz q[15], q[11];
cz q[12], q[14];
cz q[9], q[19];
cz q[8], q[17];
cz q[7], q[10];
cz q[6], q[13];
cz q[5], q[18];
cz q[4], q[16];
cz q[29], q[0];
cz q[26], q[1];
cz q[23], q[2];
cz q[21], q[3];
