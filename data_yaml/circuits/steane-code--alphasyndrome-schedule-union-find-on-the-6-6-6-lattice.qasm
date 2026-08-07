OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];
creg rec[6];

reset q[7];
reset q[8];
reset q[9];
reset q[10];
reset q[11];
reset q[12];
barrier q;

h q[8];
h q[9];
cx q[8], q[3];
cx q[9], q[0];
barrier q;

h q[7];
cx q[7], q[0];
cx q[8], q[5];
cx q[9], q[6];
barrier q;

cx q[7], q[6];
cx q[8], q[0];
cx q[9], q[4];
barrier q;

cx q[7], q[1];
cx q[9], q[2];
h q[9];
barrier q;

cx q[7], q[3];
cx q[8], q[2];
h q[7];
h q[8];
barrier q;

cx q[3], q[11];
cx q[0], q[12];
barrier q;

cx q[3], q[10];
cx q[5], q[11];
cx q[6], q[12];
barrier q;

cx q[1], q[10];
cx q[2], q[11];
cx q[4], q[12];
barrier q;

cx q[0], q[10];
cx q[2], q[12];
barrier q;

cx q[6], q[10];
cx q[0], q[11];
barrier q;

measure q[7] -> rec[0];
measure q[8] -> rec[1];
measure q[9] -> rec[2];
measure q[10] -> rec[3];
measure q[11] -> rec[4];
measure q[12] -> rec[5];
