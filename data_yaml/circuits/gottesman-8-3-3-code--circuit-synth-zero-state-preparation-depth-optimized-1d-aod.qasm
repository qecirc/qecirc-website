OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

y q[0];
h q[0];
sdg q[0];
x q[5];
h q[5];
y q[2];
h q[2];
sdg q[2];
barrier q;

swap q[5], q[0];
barrier q;

swap q[0], q[7];
barrier q;

swap q[0], q[1];
barrier q;

swap q[5], q[2];
barrier q;

y q[3];
sdg q[3];
h q[3];
sdg q[6];
h q[6];
s q[6];
h q[1];
sdg q[1];
h q[0];
sdg q[0];
sdg q[2];
sdg q[5];
cz q[6], q[5];
cz q[1], q[3];
cz q[2], q[0];
barrier q;

x q[4];
sdg q[4];
h q[4];
sdg q[7];
h q[5];
s q[5];
h q[5];
s q[3];
h q[3];
sdg q[1];
h q[2];
s q[2];
h q[2];
cz q[2], q[1];
cz q[4], q[3];
cz q[7], q[5];
barrier q;

sdg q[6];
sdg q[0];
sdg q[1];
y q[2];
sdg q[2];
h q[2];
h q[3];
sdg q[4];
y q[5];
sdg q[5];
h q[5];
sdg q[7];
cz q[4], q[2];
h q[2];
h q[4];
s q[4];
cz q[1], q[6];
h q[6];
s q[6];
h q[1];
cz q[5], q[3];
h q[5];
cz q[7], q[0];
h q[0];
