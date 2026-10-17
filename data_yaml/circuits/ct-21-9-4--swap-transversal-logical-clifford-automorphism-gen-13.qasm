OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[11];
cxyz q[9];
czyx q[7];
cxyz q[6];
cxyz q[5];
czyx q[4];
cxyz q[16];
cxyz q[12];
czyx q[13];
czyx q[10];
czyx q[14];
czyx q[18];
id q[0];
swap q[14], q[18];
swap q[13], q[20];
swap q[12], q[10];
swap q[16], q[14];
swap q[4], q[20];
swap q[6], q[13];
swap q[7], q[10];
swap q[15], q[18];
swap q[5], q[14];
swap q[8], q[7];
swap q[11], q[4];
swap q[9], q[7];
