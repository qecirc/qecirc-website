OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[9];
x q[13];
x q[12];
x q[11];
czyx q[7];
cxyz q[5];
czyx q[4];
cxyz q[3];
czyx q[8];
swap q[6], q[2];
id q[0];
czyx q[9];
cxyz q[12];
cxyz q[11];
swap q[5], q[4];
swap q[13], q[10];
swap q[12], q[8];
swap q[7], q[11];
swap q[9], q[3];
