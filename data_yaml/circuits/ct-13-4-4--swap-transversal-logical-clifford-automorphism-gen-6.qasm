OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[2];
z q[1];
czyx q[8];
czyx q[5];
cxyz q[12];
cxyz q[11];
swap q[9], q[7];
id q[0];
swap q[2], q[7];
swap q[10], q[9];
swap q[12], q[11];
swap q[3], q[7];
swap q[5], q[11];
swap q[6], q[5];
swap q[8], q[5];
