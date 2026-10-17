OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[15];
z q[13];
z q[11];
z q[10];
z q[9];
z q[8];
z q[5];
z q[3];
x q[16];
z q[14];
z q[12];
czyx q[7];
cxyz q[6];
czyx q[4];
czyx q[2];
id q[0];
cxyz q[15];
cxyz q[13];
czyx q[11];
cxyz q[5];
cxyz q[3];
czyx q[12];
swap q[8], q[14];
swap q[10], q[16];
swap q[4], q[3];
swap q[5], q[12];
swap q[11], q[6];
swap q[13], q[7];
swap q[15], q[2];
