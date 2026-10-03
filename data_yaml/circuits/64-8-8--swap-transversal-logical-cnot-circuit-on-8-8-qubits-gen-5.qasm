OPENQASM 2.0;
include "qelib1.inc";

qreg q[64];

swap q[52], q[5];
swap q[46], q[59];
swap q[45], q[54];
swap q[63], q[48];
swap q[20], q[4];
swap q[19], q[29];
swap q[18], q[27];
swap q[21], q[24];
swap q[14], q[2];
swap q[13], q[30];
swap q[12], q[28];
swap q[15], q[25];
swap q[11], q[3];
swap q[43], q[41];
swap q[40], q[38];
swap q[36], q[34];
id q[35];
