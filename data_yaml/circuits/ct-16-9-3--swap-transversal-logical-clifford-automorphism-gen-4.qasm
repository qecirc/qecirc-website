OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[9];
z q[3];
z q[2];
z q[13];
cxyz q[5];
czyx q[14];
swap q[12], q[4];
swap q[1], q[7];
id q[0];
swap q[6], q[13];
swap q[15], q[12];
swap q[2], q[7];
swap q[3], q[11];
swap q[10], q[13];
swap q[9], q[11];
