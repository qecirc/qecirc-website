OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[2];
z q[14];
czyx q[11];
czyx q[8];
cxyz q[6];
czyx q[5];
cxyz q[4];
cxyz q[10];
swap q[13], q[7];
swap q[2], q[14];
swap q[6], q[5];
swap q[8], q[10];
swap q[11], q[4];
