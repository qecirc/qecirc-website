OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

czyx q[16];
czyx q[15];
czyx q[14];
czyx q[13];
czyx q[12];
cxyz q[9];
cxyz q[8];
cxyz q[6];
cxyz q[5];
cxyz q[3];
cxyz q[2];
id q[0];
swap q[3], q[17];
swap q[6], q[1];
swap q[7], q[5];
swap q[9], q[4];
swap q[11], q[2];
swap q[12], q[3];
swap q[13], q[2];
swap q[14], q[4];
swap q[15], q[6];
swap q[16], q[5];
