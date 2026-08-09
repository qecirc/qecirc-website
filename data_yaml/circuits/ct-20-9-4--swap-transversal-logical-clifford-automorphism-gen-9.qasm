OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[14];
z q[10];
z q[8];
z q[7];
z q[5];
z q[4];
z q[3];
z q[18];
x q[15];
z q[11];
z q[16];
z q[12];
y q[9];
x q[19];
y q[13];
czyx q[6];
id q[0];
czyx q[14];
cxyz q[8];
cxyz q[5];
czyx q[4];
cxyz q[18];
czyx q[11];
cxyz q[12];
czyx q[9];
czyx q[19];
cxyz q[13];
swap q[3], q[15];
swap q[16], q[12];
swap q[18], q[13];
swap q[4], q[11];
swap q[7], q[3];
swap q[8], q[9];
swap q[5], q[18];
swap q[6], q[4];
swap q[10], q[9];
swap q[14], q[12];
