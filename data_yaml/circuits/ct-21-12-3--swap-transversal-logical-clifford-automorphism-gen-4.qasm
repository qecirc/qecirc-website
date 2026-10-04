OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[11];
czyx q[8];
cxyz q[6];
cxyz q[3];
czyx q[2];
cxyz q[14];
cxyz q[15];
czyx q[12];
czyx q[17];
czyx q[9];
cxyz q[0];
czyx q[19];
cxyz q[18];
czyx q[10];
swap q[1], q[4];
swap q[10], q[7];
swap q[17], q[20];
swap q[12], q[19];
swap q[15], q[18];
swap q[13], q[14];
swap q[16], q[1];
swap q[2], q[19];
swap q[3], q[15];
swap q[6], q[7];
swap q[8], q[13];
swap q[11], q[20];
