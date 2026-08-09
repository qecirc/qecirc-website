OPENQASM 2.0;
include "qelib1.inc";

qreg q[64];

swap q[48], q[7];
swap q[40], q[56];
swap q[39], q[49];
swap q[63], q[41];
swap q[22], q[4];
swap q[20], q[24];
swap q[19], q[23];
swap q[25], q[21];
swap q[10], q[3];
swap q[36], q[37];
swap q[33], q[34];
swap q[29], q[30];
swap q[5], q[1];
swap q[59], q[60];
swap q[52], q[53];
swap q[44], q[45];
id q[46];
