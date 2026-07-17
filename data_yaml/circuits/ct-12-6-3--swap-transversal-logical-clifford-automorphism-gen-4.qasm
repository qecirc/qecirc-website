OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

x q[11];
z q[4];
y q[10];
x q[6];
x q[8];
x q[5];
czyx q[7];
czyx q[3];
czyx q[2];
czyx q[1];
cxyz q[0];
cxyz q[11];
swap q[10], q[6];
swap q[0], q[5];
swap q[4], q[10];
swap q[11], q[9];
swap q[7], q[0];
swap q[3], q[11];
