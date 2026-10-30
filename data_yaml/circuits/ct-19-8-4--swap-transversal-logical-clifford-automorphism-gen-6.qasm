OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[9];
z q[6];
z q[5];
z q[3];
z q[16];
x q[10];
z q[12];
y q[18];
y q[8];
y q[15];
z q[17];
cxyz q[11];
czyx q[7];
czyx q[4];
cxyz q[2];
id q[0];
cxyz q[5];
czyx q[3];
czyx q[16];
cxyz q[12];
czyx q[8];
cxyz q[15];
czyx q[17];
swap q[9], q[4];
swap q[8], q[15];
swap q[10], q[17];
swap q[13], q[16];
swap q[7], q[12];
swap q[11], q[4];
swap q[18], q[8];
swap q[2], q[17];
swap q[5], q[16];
swap q[14], q[12];
