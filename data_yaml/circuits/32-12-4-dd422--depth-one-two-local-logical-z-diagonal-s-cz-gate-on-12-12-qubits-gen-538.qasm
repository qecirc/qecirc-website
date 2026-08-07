OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[29];
s q[22];
s q[14];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[16], q[1];
cz q[8], q[25];
cz q[7], q[18];
cz q[31], q[10];
cz q[6], q[2];
cz q[30], q[26];
cz q[23], q[19];
cz q[15], q[11];
cz q[4], q[3];
cz q[28], q[27];
cz q[21], q[20];
cz q[13], q[12];
