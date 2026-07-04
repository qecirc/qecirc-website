OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

s q[4];
s q[3];
h q[3];
sdg q[6];
h q[6];
s q[6];
y q[2];
sdg q[2];
h q[0];
sdg q[0];
h q[0];
s q[1];
h q[1];
barrier q;

swap q[3], q[6];
barrier q;

swap q[6], q[1];
barrier q;

swap q[0], q[2];
barrier q;

swap q[0], q[4];
barrier q;

h q[4];
sdg q[4];
h q[0];
sdg q[0];
cz q[4], q[0];
barrier q;

s q[5];
h q[5];
sdg q[5];
h q[6];
s q[6];
h q[6];
h q[2];
sdg q[2];
h q[0];
sdg q[0];
cz q[6], q[5];
cz q[2], q[0];
barrier q;

x q[7];
h q[7];
sdg q[1];
sdg q[6];
h q[0];
s q[0];
h q[0];
cz q[1], q[0];
h q[0];
s q[0];
cz q[7], q[6];
barrier q;

sdg q[3];
sdg q[4];
h q[1];
sdg q[1];
sdg q[7];
cz q[4], q[3];
cz q[1], q[7];
barrier q;

h q[5];
s q[5];
h q[5];
h q[3];
s q[3];
h q[3];
h q[4];
sdg q[4];
h q[1];
sdg q[1];
cz q[4], q[5];
cz q[1], q[3];
h q[3];
s q[3];
barrier q;

sdg q[2];
h q[6];
h q[5];
h q[1];
sdg q[1];
cz q[2], q[6];
h q[2];
cz q[1], q[5];
h q[1];
