OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[6];
z q[2];
z q[10];
s q[3];
s q[9];
h q[1];
h q[5];
h q[12];
h q[8];
sx q[0];
sx q[4];
sx q[11];
sx q[7];
s q[6];
s q[2];
s q[10];
swap q[0], q[11];
swap q[12], q[8];
swap q[3], q[10];
