OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[9];
x q[8];
x q[7];
z q[15];
z q[10];
z q[12];
z q[6];
cxyz q[5];
czyx q[11];
cxyz q[14];
czyx q[2];
cxyz q[1];
cxyz q[4];
cxyz q[13];
id q[0];
cxyz q[9];
cxyz q[8];
czyx q[15];
cxyz q[10];
cxyz q[6];
swap q[12], q[13];
swap q[6], q[4];
swap q[7], q[10];
swap q[1], q[12];
swap q[2], q[13];
swap q[15], q[4];
swap q[8], q[10];
swap q[11], q[1];
swap q[5], q[7];
swap q[14], q[15];
swap q[3], q[10];
swap q[9], q[15];
