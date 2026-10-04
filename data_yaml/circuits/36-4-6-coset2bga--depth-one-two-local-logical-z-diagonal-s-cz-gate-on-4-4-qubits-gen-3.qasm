OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

cz q[24], q[16];
cz q[20], q[13];
cz q[14], q[26];
cz q[12], q[27];
cz q[11], q[17];
cz q[10], q[19];
cz q[9], q[18];
cz q[8], q[2];
cz q[7], q[29];
cz q[6], q[22];
cz q[35], q[28];
cz q[5], q[0];
cz q[4], q[32];
cz q[23], q[33];
cz q[15], q[1];
cz q[21], q[31];
cz q[30], q[25];
cz q[34], q[3];
