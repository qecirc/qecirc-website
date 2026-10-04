OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[3];
z q[14];
z q[2];
x q[8];
z q[15];
z q[10];
y q[4];
x q[13];
cxyz q[9];
czyx q[5];
cxyz q[7];
czyx q[12];
id q[0];
czyx q[3];
cxyz q[14];
czyx q[2];
czyx q[10];
cxyz q[4];
cxyz q[13];
swap q[6], q[4];
swap q[12], q[13];
swap q[15], q[10];
swap q[14], q[8];
swap q[11], q[13];
swap q[3], q[6];
swap q[5], q[14];
swap q[9], q[10];
