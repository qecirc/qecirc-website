OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[6];
z q[18];
cxyz q[17];
czyx q[15];
cxyz q[13];
czyx q[12];
czyx q[9];
cxyz q[8];
czyx q[7];
cxyz q[5];
czyx q[4];
id q[0];
cxyz q[6];
swap q[5], q[14];
swap q[8], q[16];
swap q[10], q[9];
swap q[11], q[4];
swap q[6], q[18];
swap q[12], q[14];
swap q[13], q[9];
swap q[15], q[8];
swap q[17], q[4];
swap q[7], q[18];
