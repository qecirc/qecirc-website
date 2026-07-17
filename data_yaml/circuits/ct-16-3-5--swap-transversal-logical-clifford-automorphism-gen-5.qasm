OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[12];
z q[10];
z q[9];
z q[6];
z q[5];
z q[4];
z q[3];
y q[13];
x q[11];
czyx q[8];
czyx q[7];
cxyz q[1];
czyx q[15];
id q[0];
cxyz q[12];
cxyz q[9];
cxyz q[6];
cxyz q[4];
czyx q[13];
czyx q[11];
swap q[3], q[15];
swap q[8], q[1];
swap q[2], q[11];
swap q[4], q[15];
swap q[5], q[13];
swap q[7], q[6];
swap q[14], q[1];
swap q[9], q[11];
swap q[10], q[6];
swap q[12], q[5];
