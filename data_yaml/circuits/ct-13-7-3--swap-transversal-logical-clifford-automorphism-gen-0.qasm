OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[2];
x q[10];
x q[5];
z q[12];
z q[8];
z q[0];
y q[4];
x q[11];
z q[7];
czyx q[3];
czyx q[9];
cxyz q[1];
czyx q[2];
czyx q[10];
cxyz q[5];
cxyz q[12];
cxyz q[8];
swap q[3], q[1];
swap q[10], q[5];
swap q[9], q[8];
swap q[2], q[12];
