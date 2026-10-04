OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[13];
z q[9];
z q[7];
z q[6];
z q[5];
z q[3];
z q[10];
y q[15];
z q[8];
z q[16];
czyx q[4];
czyx q[17];
cxyz q[18];
cxyz q[12];
swap q[2], q[14];
id q[0];
czyx q[13];
czyx q[6];
cxyz q[10];
cxyz q[15];
swap q[17], q[18];
swap q[3], q[8];
swap q[7], q[11];
swap q[9], q[16];
swap q[4], q[10];
swap q[6], q[12];
swap q[13], q[15];
