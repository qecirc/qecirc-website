OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[2];
z q[1];
z q[0];
x q[6];
czyx q[7];
cxyz q[4];
czyx q[11];
cxyz q[3];
cxyz q[9];
cxyz q[8];
cxyz q[2];
cxyz q[1];
cxyz q[0];
cxyz q[6];
swap q[9], q[8];
swap q[3], q[10];
swap q[4], q[11];
swap q[0], q[6];
swap q[2], q[9];
swap q[5], q[4];
swap q[7], q[3];
swap q[1], q[0];
