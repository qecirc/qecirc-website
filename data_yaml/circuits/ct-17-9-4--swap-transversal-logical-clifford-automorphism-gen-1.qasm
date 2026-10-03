OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[11];
z q[5];
z q[4];
z q[3];
z q[2];
x q[15];
x q[8];
x q[6];
z q[16];
czyx q[1];
cxyz q[12];
czyx q[14];
swap q[0], q[10];
cxyz q[5];
cxyz q[4];
czyx q[15];
cxyz q[6];
czyx q[16];
swap q[11], q[2];
swap q[6], q[16];
swap q[15], q[12];
swap q[4], q[1];
swap q[5], q[14];
