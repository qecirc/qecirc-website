OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[8];
z q[5];
z q[3];
z q[16];
x q[13];
z q[9];
x q[10];
x q[15];
cxyz q[6];
czyx q[17];
cxyz q[11];
id q[0];
czyx q[5];
czyx q[3];
cxyz q[16];
cxyz q[13];
czyx q[10];
swap q[14], q[17];
swap q[9], q[10];
swap q[13], q[11];
swap q[3], q[17];
swap q[4], q[14];
swap q[16], q[13];
swap q[2], q[10];
swap q[5], q[4];
swap q[1], q[16];
swap q[6], q[10];
swap q[8], q[16];
swap q[12], q[10];
