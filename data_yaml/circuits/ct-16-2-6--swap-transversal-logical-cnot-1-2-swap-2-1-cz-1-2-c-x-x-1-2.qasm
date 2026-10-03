OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[14];
z q[10];
z q[8];
z q[7];
z q[4];
z q[3];
z q[1];
z q[15];
cxyz q[12];
czyx q[9];
cxyz q[6];
czyx q[5];
cxyz q[2];
czyx q[0];
cxyz q[14];
czyx q[10];
cxyz q[8];
czyx q[4];
cxyz q[1];
swap q[0], q[13];
swap q[5], q[3];
swap q[7], q[15];
swap q[2], q[0];
swap q[6], q[5];
swap q[9], q[4];
swap q[11], q[7];
swap q[12], q[1];
swap q[10], q[4];
swap q[14], q[1];
