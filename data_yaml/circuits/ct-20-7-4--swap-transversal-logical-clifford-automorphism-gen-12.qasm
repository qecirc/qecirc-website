OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[16];
z q[11];
z q[9];
z q[6];
z q[5];
z q[4];
x q[15];
z q[12];
x q[14];
x q[10];
z q[3];
czyx q[13];
czyx q[8];
czyx q[19];
czyx q[18];
sx q[2];
sx q[1];
czyx q[11];
czyx q[6];
cxyz q[5];
cxyz q[4];
cxyz q[15];
cxyz q[12];
cxyz q[14];
cxyz q[10];
swap q[1], q[0];
swap q[2], q[0];
swap q[10], q[3];
swap q[17], q[12];
swap q[15], q[18];
swap q[6], q[4];
swap q[7], q[14];
swap q[19], q[10];
swap q[9], q[18];
swap q[11], q[17];
swap q[13], q[14];
swap q[16], q[6];
