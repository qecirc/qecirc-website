OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[5];
z q[18];
z q[3];
y q[15];
z q[9];
x q[16];
czyx q[8];
cxyz q[14];
cxyz q[4];
cxyz q[6];
cxyz q[10];
czyx q[7];
id q[0];
czyx q[11];
czyx q[18];
czyx q[3];
cxyz q[15];
czyx q[9];
swap q[6], q[10];
swap q[17], q[16];
swap q[12], q[9];
swap q[3], q[15];
swap q[18], q[7];
swap q[13], q[16];
swap q[4], q[10];
swap q[14], q[9];
swap q[5], q[3];
swap q[11], q[7];
