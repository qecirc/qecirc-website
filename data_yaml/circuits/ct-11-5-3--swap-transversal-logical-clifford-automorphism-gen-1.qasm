OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[2];
x q[7];
cxyz q[6];
czyx q[4];
cxyz q[10];
czyx q[8];
czyx q[5];
cxyz q[3];
cxyz q[2];
czyx q[7];
swap q[5], q[3];
swap q[4], q[10];
swap q[6], q[8];
swap q[2], q[7];
