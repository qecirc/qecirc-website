OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[7];
z q[3];
swap q[6], q[4];
swap q[8], q[2];
swap q[9], q[1];
swap q[10], q[15];
swap q[12], q[13];
swap q[14], q[11];
id q[0];
swap q[7], q[3];
