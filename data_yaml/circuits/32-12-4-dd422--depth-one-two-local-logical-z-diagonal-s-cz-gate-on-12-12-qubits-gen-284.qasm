OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[16], q[8];
cz q[7], q[31];
cz q[6], q[25];
cz q[30], q[1];
cz q[23], q[10];
cz q[15], q[18];
cz q[5], q[29];
cz q[22], q[14];
cz q[4], q[24];
cz q[28], q[0];
cz q[21], q[9];
cz q[13], q[17];
cz q[3], q[26];
cz q[27], q[2];
cz q[20], q[11];
cz q[12], q[19];
