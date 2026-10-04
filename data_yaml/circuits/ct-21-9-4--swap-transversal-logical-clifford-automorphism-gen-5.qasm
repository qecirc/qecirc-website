OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[11];
cxyz q[7];
cxyz q[6];
czyx q[19];
czyx q[12];
cxyz q[17];
cxyz q[14];
czyx q[18];
swap q[13], q[20];
swap q[8], q[5];
id q[0];
swap q[17], q[18];
swap q[12], q[14];
swap q[7], q[19];
swap q[11], q[6];
