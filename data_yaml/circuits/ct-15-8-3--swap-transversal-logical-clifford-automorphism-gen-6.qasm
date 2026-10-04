OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[8];
z q[13];
y q[14];
z q[4];
x q[6];
z q[3];
y q[7];
czyx q[11];
cxyz q[9];
cxyz q[12];
cxyz q[2];
czyx q[1];
cxyz q[5];
id q[0];
czyx q[8];
czyx q[13];
czyx q[14];
czyx q[4];
cxyz q[6];
cxyz q[3];
swap q[1], q[5];
swap q[3], q[7];
swap q[2], q[1];
swap q[13], q[5];
swap q[6], q[3];
swap q[12], q[2];
swap q[14], q[7];
swap q[4], q[6];
swap q[10], q[12];
swap q[8], q[2];
swap q[9], q[3];
swap q[11], q[9];
