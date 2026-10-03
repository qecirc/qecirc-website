OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[15];
z q[11];
z q[10];
z q[7];
z q[6];
z q[5];
z q[16];
x q[14];
z q[12];
cxyz q[13];
czyx q[9];
czyx q[8];
cxyz q[4];
cxyz q[3];
id q[0];
cxyz q[15];
cxyz q[11];
czyx q[6];
czyx q[16];
czyx q[12];
swap q[8], q[7];
swap q[9], q[2];
swap q[3], q[12];
swap q[4], q[16];
swap q[6], q[14];
swap q[11], q[8];
swap q[15], q[9];
swap q[5], q[4];
swap q[10], q[3];
swap q[13], q[14];
