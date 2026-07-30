OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[10];
cxyz q[5];
czyx q[2];
czyx q[9];
cxyz q[20];
czyx q[12];
czyx q[8];
cxyz q[19];
czyx q[11];
cxyz q[14];
cxyz q[3];
czyx q[6];
cxyz q[4];
czyx q[7];
swap q[13], q[15];
swap q[3], q[7];
swap q[11], q[4];
swap q[19], q[6];
swap q[20], q[12];
swap q[2], q[14];
swap q[5], q[8];
swap q[10], q[9];
