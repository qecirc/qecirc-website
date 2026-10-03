OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[10];
z q[6];
z q[5];
z q[4];
z q[3];
z q[2];
z q[12];
z q[15];
y q[17];
x q[7];
czyx q[13];
czyx q[1];
cxyz q[11];
cxyz q[14];
czyx q[16];
id q[0];
cxyz q[10];
czyx q[6];
czyx q[5];
cxyz q[3];
czyx q[2];
cxyz q[12];
swap q[7], q[14];
swap q[15], q[11];
swap q[1], q[15];
swap q[3], q[16];
swap q[5], q[14];
swap q[6], q[9];
swap q[8], q[12];
swap q[4], q[16];
swap q[10], q[9];
swap q[13], q[12];
