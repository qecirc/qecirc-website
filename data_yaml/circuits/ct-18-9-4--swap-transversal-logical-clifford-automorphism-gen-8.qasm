OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[6];
z q[4];
z q[1];
y q[16];
x q[13];
z q[9];
z q[14];
x q[7];
x q[17];
x q[15];
cxyz q[5];
czyx q[2];
id q[0];
cxyz q[6];
czyx q[16];
cxyz q[13];
cxyz q[7];
czyx q[17];
czyx q[15];
swap q[11], q[15];
swap q[17], q[15];
swap q[7], q[11];
swap q[10], q[15];
swap q[14], q[11];
swap q[9], q[17];
swap q[3], q[7];
swap q[13], q[11];
swap q[16], q[14];
swap q[1], q[17];
swap q[6], q[9];
swap q[2], q[13];
swap q[4], q[17];
swap q[12], q[9];
swap q[5], q[2];
swap q[8], q[13];
