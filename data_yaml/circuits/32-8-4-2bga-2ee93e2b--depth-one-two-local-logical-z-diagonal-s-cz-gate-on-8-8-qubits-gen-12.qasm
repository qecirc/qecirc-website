OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[24], q[19];
cz q[16], q[21];
cz q[13], q[26];
cz q[10], q[8];
cz q[6], q[4];
cz q[3], q[5];
cz q[2], q[7];
cz q[1], q[0];
cz q[25], q[22];
cz q[20], q[27];
cz q[17], q[9];
cz q[14], q[11];
cz q[12], q[15];
cz q[28], q[18];
cz q[31], q[23];
cz q[30], q[29];
