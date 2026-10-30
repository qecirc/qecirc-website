OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[7];
z q[5];
z q[3];
y q[11];
z q[2];
x q[9];
czyx q[10];
cxyz q[8];
czyx q[13];
czyx q[4];
czyx q[12];
id q[0];
cxyz q[7];
czyx q[3];
czyx q[11];
czyx q[2];
czyx q[9];
swap q[5], q[13];
swap q[8], q[6];
swap q[2], q[9];
swap q[3], q[11];
swap q[7], q[13];
swap q[10], q[8];
swap q[12], q[3];
swap q[4], q[9];
