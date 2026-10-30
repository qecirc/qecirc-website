OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

cz q[20], q[38];
cz q[10], q[8];
cz q[9], q[29];
cz q[39], q[19];
cz q[7], q[36];
cz q[37], q[6];
cz q[28], q[27];
cz q[18], q[17];
cz q[5], q[31];
cz q[35], q[1];
cz q[26], q[22];
cz q[16], q[12];
cz q[4], q[32];
cz q[34], q[2];
cz q[25], q[23];
cz q[15], q[13];
cz q[3], q[30];
cz q[33], q[0];
cz q[24], q[21];
cz q[14], q[11];
