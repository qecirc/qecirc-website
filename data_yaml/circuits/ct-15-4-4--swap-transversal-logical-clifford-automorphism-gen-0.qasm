OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[5];
z q[3];
cxyz q[10];
czyx q[8];
cxyz q[14];
czyx q[13];
swap q[4], q[9];
swap q[12], q[11];
id q[0];
swap q[8], q[14];
swap q[10], q[13];
