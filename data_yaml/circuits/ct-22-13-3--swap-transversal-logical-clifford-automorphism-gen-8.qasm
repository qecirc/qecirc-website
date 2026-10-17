OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

z q[12];
z q[2];
czyx q[8];
cxyz q[4];
cxyz q[3];
czyx q[20];
cxyz q[14];
cxyz q[9];
czyx q[13];
czyx q[17];
czyx q[15];
czyx q[1];
czyx q[18];
cxyz q[6];
czyx q[11];
czyx q[21];
id q[0];
cxyz q[12];
swap q[11], q[21];
swap q[17], q[6];
swap q[13], q[18];
swap q[2], q[5];
swap q[14], q[9];
swap q[3], q[19];
swap q[1], q[21];
swap q[10], q[2];
swap q[20], q[13];
swap q[16], q[6];
swap q[8], q[3];
swap q[12], q[9];
