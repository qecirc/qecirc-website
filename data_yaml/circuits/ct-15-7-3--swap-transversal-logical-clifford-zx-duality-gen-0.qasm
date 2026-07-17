OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[14];
z q[10];
z q[2];
z q[9];
h q[8];
h q[5];
h q[4];
h q[11];
h q[12];
h q[3];
h q[7];
h q[6];
h q[13];
id q[0];
h q[14];
h q[10];
h q[2];
h q[9];
swap q[7], q[13];
swap q[4], q[11];
swap q[10], q[9];
swap q[14], q[6];
swap q[3], q[2];
