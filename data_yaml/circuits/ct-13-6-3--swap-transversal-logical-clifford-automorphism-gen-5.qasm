OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[4];
z q[1];
z q[11];
z q[6];
z q[10];
cxyz q[8];
cxyz q[3];
cxyz q[12];
czyx q[5];
czyx q[7];
id q[0];
czyx q[4];
czyx q[1];
cxyz q[11];
cxyz q[6];
swap q[7], q[10];
swap q[11], q[6];
swap q[1], q[5];
swap q[8], q[7];
swap q[12], q[6];
swap q[4], q[1];
