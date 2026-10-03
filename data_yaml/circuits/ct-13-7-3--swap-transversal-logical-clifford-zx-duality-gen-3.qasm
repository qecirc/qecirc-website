OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[3];
z q[2];
z q[1];
z q[12];
z q[11];
z q[7];
h q[6];
h q[9];
h q[10];
h q[5];
h q[8];
h q[0];
h q[4];
h q[3];
h q[2];
h q[1];
h q[12];
h q[11];
h q[7];
swap q[8], q[0];
swap q[5], q[4];
swap q[12], q[11];
swap q[1], q[7];
swap q[3], q[10];
