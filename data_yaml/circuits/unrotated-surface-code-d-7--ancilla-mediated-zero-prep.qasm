OPENQASM 2.0;
include "qelib1.inc";

qreg q[169];

h q[64];
h q[65];
h q[66];
h q[67];
h q[68];
h q[69];
h q[70];
h q[57];
h q[58];
h q[59];
h q[60];
h q[61];
h q[62];
h q[63];
h q[50];
h q[51];
h q[52];
h q[53];
h q[54];
h q[55];
h q[56];
h q[43];
h q[44];
h q[45];
h q[46];
h q[47];
h q[48];
h q[49];
h q[36];
h q[37];
h q[38];
h q[39];
h q[40];
h q[41];
h q[42];
h q[78];
h q[79];
h q[80];
h q[81];
h q[82];
h q[83];
h q[84];
barrier q;

cx q[64], q[85];
cx q[65], q[98];
cx q[66], q[111];
cx q[67], q[124];
cx q[68], q[137];
cx q[69], q[150];
cx q[70], q[163];
barrier q;

cx q[85], q[35];
cx q[98], q[29];
cx q[111], q[23];
cx q[124], q[17];
cx q[137], q[11];
cx q[150], q[5];
barrier q;

cx q[85], q[71];
cx q[98], q[72];
cx q[111], q[73];
cx q[124], q[74];
cx q[137], q[75];
cx q[150], q[76];
cx q[163], q[77];
barrier q;

cx q[98], q[35];
cx q[111], q[29];
cx q[124], q[23];
cx q[137], q[17];
cx q[150], q[11];
cx q[163], q[5];
barrier q;

cx q[64], q[85];
cx q[65], q[98];
cx q[66], q[111];
cx q[67], q[124];
cx q[68], q[137];
cx q[69], q[150];
cx q[70], q[163];
barrier q;

cx q[57], q[86];
cx q[58], q[99];
cx q[59], q[112];
cx q[60], q[125];
cx q[61], q[138];
cx q[62], q[151];
cx q[63], q[164];
barrier q;

cx q[86], q[34];
cx q[99], q[28];
cx q[112], q[22];
cx q[125], q[16];
cx q[138], q[10];
cx q[151], q[4];
barrier q;

cx q[86], q[64];
cx q[99], q[65];
cx q[112], q[66];
cx q[125], q[67];
cx q[138], q[68];
cx q[151], q[69];
cx q[164], q[70];
barrier q;

cx q[99], q[34];
cx q[112], q[28];
cx q[125], q[22];
cx q[138], q[16];
cx q[151], q[10];
cx q[164], q[4];
barrier q;

cx q[57], q[86];
cx q[58], q[99];
cx q[59], q[112];
cx q[60], q[125];
cx q[61], q[138];
cx q[62], q[151];
cx q[63], q[164];
barrier q;

cx q[50], q[87];
cx q[51], q[100];
cx q[52], q[113];
cx q[53], q[126];
cx q[54], q[139];
cx q[55], q[152];
cx q[56], q[165];
barrier q;

cx q[87], q[33];
cx q[100], q[27];
cx q[113], q[21];
cx q[126], q[15];
cx q[139], q[9];
cx q[152], q[3];
barrier q;

cx q[87], q[57];
cx q[100], q[58];
cx q[113], q[59];
cx q[126], q[60];
cx q[139], q[61];
cx q[152], q[62];
cx q[165], q[63];
barrier q;

cx q[100], q[33];
cx q[113], q[27];
cx q[126], q[21];
cx q[139], q[15];
cx q[152], q[9];
cx q[165], q[3];
barrier q;

cx q[50], q[87];
cx q[51], q[100];
cx q[52], q[113];
cx q[53], q[126];
cx q[54], q[139];
cx q[55], q[152];
cx q[56], q[165];
barrier q;

cx q[43], q[88];
cx q[44], q[101];
cx q[45], q[114];
cx q[46], q[127];
cx q[47], q[140];
cx q[48], q[153];
cx q[49], q[166];
barrier q;

cx q[88], q[32];
cx q[101], q[26];
cx q[114], q[20];
cx q[127], q[14];
cx q[140], q[8];
cx q[153], q[2];
barrier q;

cx q[88], q[50];
cx q[101], q[51];
cx q[114], q[52];
cx q[127], q[53];
cx q[140], q[54];
cx q[153], q[55];
cx q[166], q[56];
barrier q;

cx q[101], q[32];
cx q[114], q[26];
cx q[127], q[20];
cx q[140], q[14];
cx q[153], q[8];
cx q[166], q[2];
barrier q;

cx q[43], q[88];
cx q[44], q[101];
cx q[45], q[114];
cx q[46], q[127];
cx q[47], q[140];
cx q[48], q[153];
cx q[49], q[166];
barrier q;

cx q[36], q[89];
cx q[37], q[102];
cx q[38], q[115];
cx q[39], q[128];
cx q[40], q[141];
cx q[41], q[154];
cx q[42], q[167];
barrier q;

cx q[89], q[31];
cx q[102], q[25];
cx q[115], q[19];
cx q[128], q[13];
cx q[141], q[7];
cx q[154], q[1];
barrier q;

cx q[89], q[43];
cx q[102], q[44];
cx q[115], q[45];
cx q[128], q[46];
cx q[141], q[47];
cx q[154], q[48];
cx q[167], q[49];
barrier q;

cx q[102], q[31];
cx q[115], q[25];
cx q[128], q[19];
cx q[141], q[13];
cx q[154], q[7];
cx q[167], q[1];
barrier q;

cx q[36], q[89];
cx q[37], q[102];
cx q[38], q[115];
cx q[39], q[128];
cx q[40], q[141];
cx q[41], q[154];
cx q[42], q[167];
barrier q;

cx q[78], q[90];
cx q[79], q[103];
cx q[80], q[116];
cx q[81], q[129];
cx q[82], q[142];
cx q[83], q[155];
cx q[84], q[168];
barrier q;

cx q[90], q[30];
cx q[103], q[24];
cx q[116], q[18];
cx q[129], q[12];
cx q[142], q[6];
cx q[155], q[0];
barrier q;

cx q[90], q[36];
cx q[103], q[37];
cx q[116], q[38];
cx q[129], q[39];
cx q[142], q[40];
cx q[155], q[41];
cx q[168], q[42];
barrier q;

cx q[103], q[30];
cx q[116], q[24];
cx q[129], q[18];
cx q[142], q[12];
cx q[155], q[6];
cx q[168], q[0];
barrier q;

cx q[78], q[90];
cx q[79], q[103];
cx q[80], q[116];
cx q[81], q[129];
cx q[82], q[142];
cx q[83], q[155];
cx q[84], q[168];
barrier q;

