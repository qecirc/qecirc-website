OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[13];
z q[6];
z q[5];
z q[2];
z q[14];
y q[10];
z q[15];
y q[11];
z q[18];
x q[16];
cxyz q[9];
cxyz q[7];
czyx q[4];
cxyz q[17];
czyx q[8];
czyx q[12];
id q[0];
czyx q[2];
cxyz q[11];
swap q[14], q[15];
swap q[17], q[8];
swap q[7], q[12];
swap q[9], q[4];
swap q[13], q[6];
swap q[2], q[11];
