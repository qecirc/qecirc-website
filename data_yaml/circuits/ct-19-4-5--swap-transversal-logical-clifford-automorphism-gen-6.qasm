OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

z q[9];
z q[8];
z q[5];
z q[12];
z q[10];
z q[17];
swap q[14], q[16];
id q[0];
swap q[18], q[10];
swap q[15], q[12];
swap q[5], q[14];
swap q[3], q[18];
swap q[4], q[15];
swap q[8], q[5];
swap q[6], q[3];
swap q[7], q[4];
swap q[13], q[8];
swap q[9], q[6];
swap q[11], q[7];
