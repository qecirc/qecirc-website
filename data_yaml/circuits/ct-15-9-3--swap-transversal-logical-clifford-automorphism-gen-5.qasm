OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[4];
z q[2];
x q[10];
z q[13];
z q[0];
y q[6];
y q[14];
z q[9];
x q[11];
z q[3];
z q[12];
cxyz q[1];
cxyz q[7];
cxyz q[5];
cxyz q[4];
czyx q[2];
czyx q[13];
cxyz q[0];
czyx q[6];
czyx q[9];
czyx q[11];
swap q[1], q[14];
swap q[11], q[5];
swap q[9], q[12];
swap q[7], q[6];
swap q[13], q[14];
swap q[2], q[3];
swap q[0], q[12];
swap q[10], q[7];
swap q[4], q[3];
swap q[8], q[11];
