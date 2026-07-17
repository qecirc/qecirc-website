OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[13], q[17];
id q[0];
swap q[19], q[17];
swap q[9], q[13];
swap q[12], q[19];
swap q[16], q[9];
swap q[15], q[17];
swap q[18], q[13];
swap q[11], q[12];
swap q[3], q[19];
swap q[4], q[9];
swap q[6], q[17];
swap q[7], q[13];
swap q[5], q[12];
swap q[8], q[19];
swap q[10], q[9];
swap q[14], q[12];
