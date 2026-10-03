OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[16], q[5];
cz q[8], q[29];
cz q[7], q[22];
cz q[31], q[14];
cz q[6], q[4];
cz q[30], q[28];
cz q[23], q[21];
cz q[15], q[13];
cz q[3], q[0];
cz q[27], q[24];
cz q[20], q[17];
cz q[12], q[9];
cz q[2], q[1];
cz q[26], q[25];
cz q[19], q[18];
cz q[11], q[10];
