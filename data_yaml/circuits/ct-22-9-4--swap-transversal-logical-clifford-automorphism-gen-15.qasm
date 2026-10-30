OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[12];
czyx q[9];
czyx q[6];
cxyz q[20];
cxyz q[17];
cxyz q[14];
cxyz q[11];
czyx q[15];
id q[0];
swap q[11], q[19];
swap q[13], q[15];
swap q[20], q[18];
swap q[14], q[11];
swap q[5], q[13];
swap q[10], q[20];
swap q[12], q[18];
swap q[17], q[11];
swap q[6], q[13];
swap q[16], q[20];
swap q[8], q[17];
swap q[9], q[6];
