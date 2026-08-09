OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[9];
x q[14];
z q[15];
z q[2];
z q[7];
x q[8];
y q[6];
czyx q[12];
cxyz q[10];
czyx q[11];
cxyz q[3];
czyx q[4];
id q[0];
czyx q[9];
cxyz q[14];
czyx q[15];
czyx q[2];
cxyz q[7];
cxyz q[8];
cxyz q[6];
swap q[4], q[8];
swap q[2], q[6];
swap q[7], q[8];
swap q[3], q[6];
swap q[15], q[4];
swap q[14], q[2];
swap q[5], q[8];
swap q[13], q[6];
swap q[10], q[7];
swap q[11], q[6];
swap q[9], q[13];
swap q[12], q[7];
