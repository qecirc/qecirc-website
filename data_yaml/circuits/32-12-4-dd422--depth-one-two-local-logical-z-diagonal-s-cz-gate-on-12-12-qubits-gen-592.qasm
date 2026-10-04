OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[16], q[8];
cz q[7], q[31];
cz q[6], q[30];
cz q[23], q[15];
cz q[5], q[28];
cz q[29], q[4];
cz q[22], q[13];
cz q[14], q[21];
cz q[3], q[27];
cz q[20], q[12];
cz q[2], q[26];
cz q[19], q[11];
cz q[1], q[24];
cz q[25], q[0];
cz q[18], q[9];
cz q[10], q[17];
