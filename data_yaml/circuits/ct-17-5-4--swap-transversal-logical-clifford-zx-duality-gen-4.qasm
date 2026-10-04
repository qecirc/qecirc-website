OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[7];
z q[3];
z q[14];
z q[12];
swap q[6], q[13];
swap q[16], q[15];
id q[0];
swap q[8], q[14];
swap q[4], q[3];
swap q[5], q[6];
swap q[9], q[15];
swap q[7], q[8];
swap q[11], q[3];
