OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[7];
z q[3];
z q[2];
y q[11];
z q[9];
z q[10];
x q[4];
cxyz q[5];
cxyz q[8];
czyx q[1];
cxyz q[6];
id q[0];
czyx q[2];
cxyz q[9];
czyx q[10];
swap q[1], q[11];
swap q[9], q[10];
swap q[2], q[8];
swap q[5], q[1];
swap q[3], q[2];
swap q[7], q[10];
