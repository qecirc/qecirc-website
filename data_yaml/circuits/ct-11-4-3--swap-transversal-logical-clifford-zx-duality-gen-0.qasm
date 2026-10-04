OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[3];
z q[2];
swap q[6], q[7];
swap q[1], q[4];
swap q[9], q[10];
id q[0];
swap q[3], q[2];
