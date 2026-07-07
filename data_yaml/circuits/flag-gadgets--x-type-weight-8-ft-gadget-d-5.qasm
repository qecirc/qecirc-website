OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];
creg rec[3];

h q[0];
cx q[0], q[10];
cx q[0], q[9];
cx q[0], q[8];
cx q[9], q[5];
cx q[0], q[7];
cx q[9], q[4];
cx q[0], q[6];
cx q[0], q[10];
cx q[0], q[3];
measure q[10] -> rec[0];
cx q[0], q[2];
cx q[0], q[9];
cx q[0], q[1];
measure q[9] -> rec[1];
cx q[0], q[8];
measure q[8] -> rec[2];
