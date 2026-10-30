OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[9];
x q[17];
x q[10];
z q[11];
y q[8];
y q[18];
y q[12];
z q[16];
cxyz q[13];
czyx q[7];
cxyz q[3];
czyx q[2];
swap q[5], q[15];
id q[0];
czyx q[9];
cxyz q[17];
czyx q[11];
czyx q[8];
cxyz q[18];
cxyz q[12];
cxyz q[16];
swap q[3], q[14];
swap q[6], q[5];
swap q[12], q[16];
swap q[10], q[8];
swap q[2], q[11];
swap q[7], q[3];
swap q[17], q[12];
swap q[9], q[2];
swap q[13], q[10];
