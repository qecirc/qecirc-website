OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];
creg rec[2];

reset q[4]; h q[4]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
barrier q;

cx q[4], q[0];
barrier q;

cx q[4], q[1];
barrier q;

cx q[4], q[3];
barrier q;

cx q[4], q[2];
barrier q;

barrier q;

cz q[5], q[1];
barrier q;

cz q[5], q[2];
barrier q;

cz q[5], q[3];
barrier q;

cz q[5], q[0];
barrier q;

h q[4]; measure q[4] -> rec[0]; h q[4]; // decomposed MX
h q[5]; measure q[5] -> rec[1]; h q[5]; // decomposed MX
