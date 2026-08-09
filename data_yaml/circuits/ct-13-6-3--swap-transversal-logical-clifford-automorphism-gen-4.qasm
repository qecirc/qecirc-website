OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[3];
x q[12];
z q[5];
x q[11];
czyx q[4];
cxyz q[1];
czyx q[9];
czyx q[10];
id q[0];
cxyz q[3];
czyx q[12];
cxyz q[5];
cxyz q[11];
swap q[6], q[10];
swap q[5], q[10];
swap q[12], q[7];
swap q[4], q[11];
swap q[1], q[7];
swap q[8], q[11];
