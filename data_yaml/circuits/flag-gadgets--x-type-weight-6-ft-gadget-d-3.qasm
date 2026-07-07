OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];
creg rec[1];

h q[0];
cx q[0], q[6];
cx q[0], q[5];
cx q[0], q[4];
cx q[0], q[3];
cx q[0], q[2];
cx q[0], q[1];
cx q[0], q[6];
measure q[6] -> rec[0];
