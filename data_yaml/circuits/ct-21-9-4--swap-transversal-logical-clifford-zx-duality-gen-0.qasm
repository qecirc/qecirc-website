OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[13], q[20];
swap q[17], q[14];
swap q[12], q[18];
swap q[5], q[4];
id q[0];
swap q[16], q[13];
swap q[19], q[18];
swap q[6], q[17];
swap q[7], q[14];
swap q[8], q[5];
swap q[11], q[12];
swap q[15], q[20];
swap q[9], q[5];
