OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[11];
cxyz q[7];
czyx q[3];
czyx q[2];
cxyz q[9];
cxyz q[13];
czyx q[1];
cxyz q[18];
czyx q[12];
czyx q[4];
cxyz q[14];
cxyz q[0];
cxyz q[17];
czyx q[10];
swap q[15], q[5];
id q[20];
swap q[0], q[10];
swap q[12], q[17];
swap q[18], q[4];
swap q[2], q[9];
swap q[3], q[14];
swap q[7], q[1];
swap q[11], q[13];
