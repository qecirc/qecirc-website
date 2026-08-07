OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

cz q[14], q[16];
cz q[10], q[4];
cz q[8], q[9];
cz q[6], q[18];
cz q[5], q[20];
cz q[3], q[2];
cz q[1], q[21];
cz q[0], q[17];
cz q[7], q[13];
cz q[15], q[12];
cz q[11], q[19];
