OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[5];
z q[3];
z q[2];
x q[11];
cxyz q[8];
czyx q[6];
cxyz q[10];
id q[0];
cxyz q[3];
czyx q[2];
czyx q[11];
swap q[10], q[4];
swap q[6], q[10];
swap q[1], q[11];
swap q[9], q[10];
swap q[8], q[1];
swap q[7], q[6];
swap q[2], q[8];
swap q[3], q[8];
