OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];
creg rec[8];

reset q[9];
reset q[10];
reset q[11];
reset q[12];
reset q[13];
reset q[14];
reset q[15];
reset q[16];
barrier q;

h q[9];
h q[10];
h q[11];
cx q[9], q[7];
cx q[10], q[6];
cx q[11], q[4];
cx q[0], q[14];
cx q[2], q[15];
barrier q;

cx q[10], q[2];
cx q[11], q[0];
cx q[6], q[13];
cx q[5], q[14];
cx q[8], q[15];
cx q[4], q[16];
barrier q;

h q[12];
cx q[9], q[1];
cx q[10], q[5];
cx q[11], q[3];
cx q[12], q[2];
cx q[7], q[14];
cx q[0], q[15];
h q[9];
barrier q;

cx q[10], q[0];
cx q[11], q[7];
cx q[12], q[8];
cx q[5], q[13];
cx q[1], q[14];
cx q[4], q[15];
cx q[3], q[16];
h q[10];
h q[11];
h q[12];
barrier q;

measure q[9] -> rec[0];
measure q[10] -> rec[1];
measure q[11] -> rec[2];
measure q[12] -> rec[3];
measure q[13] -> rec[4];
measure q[14] -> rec[5];
measure q[15] -> rec[6];
measure q[16] -> rec[7];
