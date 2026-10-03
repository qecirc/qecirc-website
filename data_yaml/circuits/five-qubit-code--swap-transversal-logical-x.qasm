OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

sx q[3];
sx q[2];
sx q[1];
sx q[0];
sx q[4];
swap q[0], q[4];
swap q[1], q[0];
swap q[2], q[0];
