OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

s q[4];
h q[4];
h q[2];
h q[3];
s q[3];
h q[1];
sdg q[0];
barrier q;

swap q[4], q[0];
barrier q;

swap q[4], q[2];
barrier q;

swap q[1], q[3];
barrier q;

sdg q[3];
sdg q[1];
cz q[3], q[1];
barrier q;

sdg q[4];
h q[1];
s q[1];
h q[1];
cz q[1], q[4];
barrier q;

sdg q[0];
h q[2];
sdg q[2];
sdg q[4];
y q[1];
sdg q[1];
h q[1];
cz q[2], q[4];
cz q[1], q[0];
h q[1];
barrier q;

h q[2];
sdg q[2];
h q[0];
s q[0];
h q[0];
cz q[2], q[0];
barrier q;

sdg q[3];
h q[0];
cz q[3], q[0];
