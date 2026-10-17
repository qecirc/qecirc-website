OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[9];
z q[6];
z q[5];
z q[3];
z q[2];
y q[13];
x q[15];
y q[10];
y q[12];
z q[8];
z q[16];
swap q[14], q[11];
id q[0];
czyx q[9];
cxyz q[5];
cxyz q[13];
czyx q[15];
czyx q[12];
cxyz q[16];
swap q[4], q[10];
swap q[7], q[2];
swap q[15], q[16];
swap q[13], q[12];
swap q[9], q[5];
