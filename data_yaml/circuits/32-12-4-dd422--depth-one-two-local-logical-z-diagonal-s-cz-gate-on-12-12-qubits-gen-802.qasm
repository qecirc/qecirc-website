OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[16], q[6];
cz q[8], q[23];
cz q[7], q[30];
cz q[31], q[15];
cz q[5], q[4];
cz q[29], q[21];
cz q[22], q[28];
cz q[14], q[13];
cz q[3], q[2];
cz q[27], q[19];
cz q[20], q[26];
cz q[12], q[11];
cz q[1], q[0];
cz q[25], q[17];
cz q[18], q[24];
cz q[10], q[9];
