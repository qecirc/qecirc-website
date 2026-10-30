OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[2];
czyx q[13];
cxyz q[9];
czyx q[20];
cxyz q[8];
czyx q[19];
czyx q[11];
cxyz q[14];
czyx q[3];
cxyz q[6];
cxyz q[15];
czyx q[4];
swap q[12], q[18];
swap q[1], q[7];
swap q[14], q[15];
swap q[11], q[17];
swap q[19], q[4];
swap q[0], q[6];
swap q[5], q[1];
swap q[10], q[18];
swap q[20], q[4];
swap q[9], q[15];
swap q[13], q[0];
swap q[2], q[17];
