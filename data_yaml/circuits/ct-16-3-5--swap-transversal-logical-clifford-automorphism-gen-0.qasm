OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[10];
z q[9];
z q[4];
z q[2];
z q[15];
z q[13];
y q[11];
cxyz q[14];
cxyz q[5];
cxyz q[3];
czyx q[1];
id q[0];
czyx q[4];
czyx q[13];
swap q[2], q[11];
swap q[10], q[7];
swap q[14], q[1];
swap q[4], q[3];
swap q[5], q[13];
