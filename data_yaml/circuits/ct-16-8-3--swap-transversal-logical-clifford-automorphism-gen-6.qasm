OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[14];
z q[13];
z q[5];
z q[3];
cxyz q[10];
czyx q[9];
czyx q[15];
czyx q[2];
cxyz q[7];
cxyz q[6];
swap q[11], q[4];
id q[0];
swap q[2], q[7];
swap q[3], q[8];
swap q[9], q[5];
swap q[12], q[11];
swap q[13], q[2];
swap q[14], q[3];
swap q[10], q[9];
