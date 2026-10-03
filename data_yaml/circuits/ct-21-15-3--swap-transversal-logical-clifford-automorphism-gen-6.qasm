OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[5];
czyx q[2];
czyx q[13];
czyx q[16];
cxyz q[1];
cxyz q[9];
cxyz q[20];
cxyz q[12];
czyx q[0];
czyx q[8];
czyx q[19];
czyx q[11];
czyx q[17];
czyx q[14];
czyx q[3];
czyx q[6];
id q[7];
swap q[11], q[6];
swap q[19], q[14];
swap q[8], q[17];
swap q[0], q[3];
swap q[9], q[20];
swap q[1], q[20];
swap q[16], q[6];
swap q[13], q[17];
swap q[2], q[3];
swap q[5], q[14];
