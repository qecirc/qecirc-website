OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

cxyz q[9];
czyx q[3];
cxyz q[2];
czyx q[11];
czyx q[16];
czyx q[10];
czyx q[15];
czyx q[13];
cxyz q[4];
czyx q[14];
cxyz q[8];
id q[0];
swap q[14], q[5];
swap q[7], q[4];
swap q[13], q[8];
swap q[15], q[14];
swap q[10], q[4];
swap q[11], q[8];
swap q[3], q[5];
swap q[16], q[4];
swap q[12], q[14];
swap q[6], q[8];
swap q[2], q[4];
swap q[9], q[8];
