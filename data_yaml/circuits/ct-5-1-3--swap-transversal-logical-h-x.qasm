OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[5];

czyx q[1];
czyx q[0];
czyx q[3];
czyx q[4];
swap q[0], q[3];
swap q[1], q[0];
