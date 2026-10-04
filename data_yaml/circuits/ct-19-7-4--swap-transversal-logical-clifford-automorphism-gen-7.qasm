OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[15];
z q[10];
z q[8];
z q[7];
z q[5];
z q[4];
z q[14];
x q[16];
x q[11];
z q[13];
z q[9];
x q[17];
czyx q[6];
cxyz q[18];
czyx q[2];
id q[0];
czyx q[15];
cxyz q[5];
czyx q[16];
czyx q[11];
cxyz q[13];
cxyz q[9];
czyx q[17];
swap q[3], q[14];
swap q[9], q[2];
swap q[13], q[17];
swap q[5], q[16];
swap q[6], q[11];
swap q[12], q[14];
swap q[7], q[2];
swap q[8], q[16];
swap q[10], q[17];
swap q[15], q[11];
