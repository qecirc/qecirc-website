OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[5];
cxyz q[2];
cxyz q[13];
cxyz q[16];
czyx q[1];
czyx q[9];
czyx q[20];
czyx q[12];
cxyz q[0];
cxyz q[8];
cxyz q[19];
cxyz q[11];
czyx q[17];
czyx q[14];
cxyz q[3];
swap q[4], q[7];
swap q[6], q[18];
swap q[3], q[15];
swap q[14], q[4];
swap q[19], q[6];
swap q[8], q[18];
swap q[17], q[14];
swap q[11], q[15];
swap q[0], q[8];
swap q[9], q[3];
swap q[13], q[4];
swap q[12], q[15];
swap q[1], q[0];
swap q[16], q[11];
swap q[2], q[14];
swap q[20], q[12];
swap q[5], q[1];
swap q[10], q[2];
