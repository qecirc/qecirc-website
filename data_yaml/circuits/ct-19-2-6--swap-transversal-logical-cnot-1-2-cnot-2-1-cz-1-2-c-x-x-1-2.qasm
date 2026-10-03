OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[15];
z q[13];
z q[12];
z q[9];
z q[8];
z q[6];
z q[3];
x q[16];
z q[18];
czyx q[14];
cxyz q[11];
cxyz q[10];
czyx q[7];
czyx q[4];
id q[0];
czyx q[15];
cxyz q[13];
cxyz q[12];
cxyz q[9];
czyx q[8];
czyx q[18];
swap q[7], q[16];
swap q[11], q[4];
swap q[3], q[18];
swap q[8], q[5];
swap q[10], q[16];
swap q[12], q[6];
swap q[17], q[11];
swap q[9], q[3];
swap q[13], q[5];
swap q[14], q[12];
