OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[1];

h q[0];
cx q[0], q[9];
cx q[0], q[8];
cx q[0], q[7];
cx q[0], q[6];
cx q[0], q[5];
cx q[0], q[4];
cx q[0], q[3];
cx q[0], q[2];
cx q[0], q[1];
cx q[0], q[9];
measure q[9] -> rec[0];
