OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[3];
z q[2];
cxyz q[9];
czyx q[13];
czyx q[5];
cxyz q[12];
id q[0];
swap q[2], q[8];
swap q[5], q[12];
swap q[10], q[8];
swap q[11], q[2];
swap q[13], q[5];
swap q[7], q[12];
swap q[3], q[8];
swap q[9], q[12];
