OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

x q[1];
barrier q;

h q[4];
s q[4];
h q[4];
x q[2];
h q[2];
barrier q;

swap q[4], q[1];
barrier q;

swap q[1], q[2];
barrier q;

h q[4];
sdg q[4];
h q[1];
s q[1];
h q[1];
cz q[1], q[4];
h q[1];
s q[1];
barrier q;

h q[0];
z q[3];
h q[3];
sdg q[3];
h q[2];
sdg q[2];
s q[4];
h q[4];
cz q[0], q[4];
cz q[3], q[2];
barrier q;

h q[4];
sdg q[0];
s q[2];
h q[2];
y q[3];
sdg q[3];
h q[3];
cz q[3], q[0];
h q[0];
h q[3];
cz q[2], q[4];
h q[2];
s q[2];
