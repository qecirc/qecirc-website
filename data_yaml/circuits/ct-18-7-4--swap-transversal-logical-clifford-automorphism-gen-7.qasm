OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[11];
z q[9];
z q[6];
z q[5];
x q[13];
y q[15];
z q[17];
z q[16];
cxyz q[14];
cxyz q[7];
czyx q[4];
cxyz q[3];
czyx q[10];
czyx q[8];
cxyz q[1];
id q[0];
czyx q[11];
cxyz q[9];
cxyz q[5];
czyx q[16];
swap q[8], q[1];
swap q[15], q[10];
swap q[4], q[2];
swap q[13], q[16];
swap q[5], q[12];
swap q[6], q[8];
swap q[9], q[10];
swap q[14], q[2];
swap q[7], q[13];
swap q[11], q[5];
