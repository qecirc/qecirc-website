OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[16];
z q[13];
z q[7];
z q[6];
z q[5];
z q[4];
z q[12];
y q[14];
x q[19];
x q[10];
z q[18];
cxyz q[11];
cxyz q[9];
czyx q[15];
id q[0];
czyx q[16];
czyx q[7];
czyx q[6];
czyx q[4];
cxyz q[12];
cxyz q[14];
cxyz q[18];
swap q[13], q[17];
swap q[15], q[12];
swap q[6], q[14];
swap q[9], q[7];
swap q[11], q[4];
swap q[16], q[18];
