OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[8];
z q[6];
z q[5];
x q[10];
z q[3];
z q[1];
y q[4];
cxyz q[9];
cxyz q[7];
czyx q[2];
czyx q[0];
cxyz q[8];
cxyz q[6];
cxyz q[5];
cxyz q[10];
czyx q[3];
czyx q[1];
czyx q[4];
swap q[2], q[1];
swap q[5], q[10];
swap q[3], q[2];
swap q[6], q[5];
