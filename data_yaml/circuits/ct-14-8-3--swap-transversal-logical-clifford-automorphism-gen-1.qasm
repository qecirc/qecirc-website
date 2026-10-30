OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[10];
z q[7];
z q[12];
z q[9];
y q[13];
x q[11];
z q[5];
z q[4];
czyx q[3];
cxyz q[1];
cxyz q[2];
swap q[8], q[0];
czyx q[10];
czyx q[12];
cxyz q[11];
swap q[3], q[2];
swap q[9], q[5];
swap q[7], q[6];
swap q[12], q[11];
swap q[10], q[1];
