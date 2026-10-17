OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

czyx q[16];
czyx q[12];
cxyz q[10];
czyx q[9];
czyx q[7];
cxyz q[6];
czyx q[5];
czyx q[20];
czyx q[17];
cxyz q[13];
cxyz q[18];
cxyz q[14];
cxyz q[11];
cxyz q[21];
cxyz q[15];
czyx q[19];
id q[0];
swap q[14], q[19];
swap q[17], q[11];
swap q[20], q[15];
swap q[6], q[5];
swap q[7], q[18];
swap q[9], q[21];
swap q[12], q[10];
swap q[16], q[13];
