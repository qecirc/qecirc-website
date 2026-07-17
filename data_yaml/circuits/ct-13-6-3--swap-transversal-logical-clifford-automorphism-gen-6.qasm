OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[3];
z q[1];
z q[5];
x q[11];
z q[6];
czyx q[2];
cxyz q[12];
czyx q[7];
czyx q[10];
id q[0];
cxyz q[8];
czyx q[1];
cxyz q[5];
czyx q[11];
cxyz q[6];
swap q[7], q[6];
swap q[11], q[10];
swap q[12], q[5];
swap q[1], q[11];
swap q[4], q[6];
swap q[8], q[5];
