OPENQASM 2.0;
include "qelib1.inc";

qreg q[236];

h q[100];
h q[90];
h q[89];
h q[82];
h q[81];
h q[76];
h q[75];
h q[72];
h q[71];
h q[70];
h q[120];
h q[69];
h q[68];
h q[67];
h q[66];
h q[65];
h q[103];
h q[92];
h q[84];
h q[78];
h q[74];
h q[51];
h q[50];
h q[49];
h q[48];
h q[47];
h q[58];
h q[105];
h q[94];
h q[86];
h q[80];
h q[35];
h q[34];
h q[33];
h q[32];
h q[31];
h q[42];
h q[60];
h q[107];
h q[96];
h q[88];
h q[21];
h q[20];
h q[19];
h q[18];
h q[17];
h q[28];
h q[44];
h q[62];
h q[109];
h q[98];
h q[9];
h q[8];
h q[7];
h q[6];
h q[5];
h q[16];
h q[30];
h q[46];
h q[64];
h q[111];
h q[126];
h q[148];
h q[170];
h q[192];
h q[214];
h q[147];
h q[169];
h q[191];
h q[213];
h q[235];
h q[128];
h q[130];
h q[132];
h q[134];
h q[136];
h q[137];
h q[139];
h q[141];
h q[143];
h q[145];
h q[150];
h q[152];
h q[154];
h q[156];
h q[158];
h q[159];
h q[161];
h q[163];
h q[165];
h q[167];
h q[172];
h q[174];
h q[176];
h q[178];
h q[180];
h q[181];
h q[183];
h q[185];
h q[187];
h q[189];
h q[194];
h q[196];
h q[198];
h q[200];
h q[202];
h q[203];
h q[205];
h q[207];
h q[209];
h q[211];
h q[216];
h q[218];
h q[220];
h q[222];
h q[224];
h q[225];
h q[227];
h q[229];
h q[231];
h q[233];
barrier q;

cx q[126], q[99];
cx q[128], q[91];
cx q[130], q[83];
cx q[132], q[77];
cx q[134], q[73];
cx q[136], q[118];
barrier q;

cx q[100], q[126];
cx q[89], q[128];
cx q[81], q[130];
cx q[75], q[132];
cx q[71], q[134];
cx q[120], q[136];
barrier q;

cx q[90], q[128];
cx q[82], q[130];
cx q[76], q[132];
cx q[72], q[134];
cx q[70], q[136];
barrier q;

cx q[69], q[128];
cx q[68], q[130];
cx q[67], q[132];
cx q[66], q[134];
cx q[65], q[136];
barrier q;

cx q[126], q[99];
cx q[128], q[91];
cx q[130], q[83];
cx q[132], q[77];
cx q[134], q[73];
cx q[136], q[118];
barrier q;

cx q[147], q[119];
cx q[145], q[52];
cx q[143], q[53];
cx q[141], q[54];
cx q[139], q[55];
cx q[137], q[57];
barrier q;

cx q[118], q[147];
cx q[73], q[145];
cx q[77], q[143];
cx q[83], q[141];
cx q[91], q[139];
cx q[99], q[137];
barrier q;

cx q[65], q[145];
cx q[66], q[143];
cx q[67], q[141];
cx q[68], q[139];
cx q[69], q[137];
barrier q;

cx q[74], q[145];
cx q[78], q[143];
cx q[84], q[141];
cx q[92], q[139];
cx q[103], q[137];
barrier q;

cx q[147], q[119];
cx q[145], q[52];
cx q[143], q[53];
cx q[141], q[54];
cx q[139], q[55];
cx q[137], q[57];
barrier q;

cx q[148], q[56];
cx q[150], q[104];
cx q[152], q[93];
cx q[154], q[85];
cx q[156], q[79];
cx q[158], q[116];
barrier q;

cx q[57], q[148];
cx q[55], q[150];
cx q[54], q[152];
cx q[53], q[154];
cx q[52], q[156];
cx q[119], q[158];
barrier q;

cx q[103], q[150];
cx q[92], q[152];
cx q[84], q[154];
cx q[78], q[156];
cx q[74], q[158];
barrier q;

cx q[51], q[150];
cx q[50], q[152];
cx q[49], q[154];
cx q[48], q[156];
cx q[47], q[158];
barrier q;

cx q[148], q[56];
cx q[150], q[104];
cx q[152], q[93];
cx q[154], q[85];
cx q[156], q[79];
cx q[158], q[116];
barrier q;

cx q[169], q[117];
cx q[167], q[36];
cx q[165], q[37];
cx q[163], q[38];
cx q[161], q[39];
cx q[159], q[41];
barrier q;

cx q[116], q[169];
cx q[79], q[167];
cx q[85], q[165];
cx q[93], q[163];
cx q[104], q[161];
cx q[56], q[159];
barrier q;

cx q[47], q[167];
cx q[48], q[165];
cx q[49], q[163];
cx q[50], q[161];
cx q[51], q[159];
barrier q;

cx q[80], q[167];
cx q[86], q[165];
cx q[94], q[163];
cx q[105], q[161];
cx q[58], q[159];
barrier q;

cx q[169], q[117];
cx q[167], q[36];
cx q[165], q[37];
cx q[163], q[38];
cx q[161], q[39];
cx q[159], q[41];
barrier q;

cx q[170], q[40];
cx q[172], q[59];
cx q[174], q[106];
cx q[176], q[95];
cx q[178], q[87];
cx q[180], q[114];
barrier q;

cx q[41], q[170];
cx q[39], q[172];
cx q[38], q[174];
cx q[37], q[176];
cx q[36], q[178];
cx q[117], q[180];
barrier q;

cx q[58], q[172];
cx q[105], q[174];
cx q[94], q[176];
cx q[86], q[178];
cx q[80], q[180];
barrier q;

cx q[35], q[172];
cx q[34], q[174];
cx q[33], q[176];
cx q[32], q[178];
cx q[31], q[180];
barrier q;

cx q[170], q[40];
cx q[172], q[59];
cx q[174], q[106];
cx q[176], q[95];
cx q[178], q[87];
cx q[180], q[114];
barrier q;

cx q[191], q[115];
cx q[189], q[22];
cx q[187], q[23];
cx q[185], q[24];
cx q[183], q[25];
cx q[181], q[27];
barrier q;

cx q[114], q[191];
cx q[87], q[189];
cx q[95], q[187];
cx q[106], q[185];
cx q[59], q[183];
cx q[40], q[181];
barrier q;

cx q[31], q[189];
cx q[32], q[187];
cx q[33], q[185];
cx q[34], q[183];
cx q[35], q[181];
barrier q;

cx q[88], q[189];
cx q[96], q[187];
cx q[107], q[185];
cx q[60], q[183];
cx q[42], q[181];
barrier q;

cx q[191], q[115];
cx q[189], q[22];
cx q[187], q[23];
cx q[185], q[24];
cx q[183], q[25];
cx q[181], q[27];
barrier q;

cx q[192], q[26];
cx q[194], q[43];
cx q[196], q[61];
cx q[198], q[108];
cx q[200], q[97];
cx q[202], q[112];
barrier q;

cx q[27], q[192];
cx q[25], q[194];
cx q[24], q[196];
cx q[23], q[198];
cx q[22], q[200];
cx q[115], q[202];
barrier q;

cx q[42], q[194];
cx q[60], q[196];
cx q[107], q[198];
cx q[96], q[200];
cx q[88], q[202];
barrier q;

cx q[21], q[194];
cx q[20], q[196];
cx q[19], q[198];
cx q[18], q[200];
cx q[17], q[202];
barrier q;

cx q[192], q[26];
cx q[194], q[43];
cx q[196], q[61];
cx q[198], q[108];
cx q[200], q[97];
cx q[202], q[112];
barrier q;

cx q[213], q[113];
cx q[211], q[10];
cx q[209], q[11];
cx q[207], q[12];
cx q[205], q[13];
cx q[203], q[15];
barrier q;

cx q[112], q[213];
cx q[97], q[211];
cx q[108], q[209];
cx q[61], q[207];
cx q[43], q[205];
cx q[26], q[203];
barrier q;

cx q[17], q[211];
cx q[18], q[209];
cx q[19], q[207];
cx q[20], q[205];
cx q[21], q[203];
barrier q;

cx q[98], q[211];
cx q[109], q[209];
cx q[62], q[207];
cx q[44], q[205];
cx q[28], q[203];
barrier q;

cx q[213], q[113];
cx q[211], q[10];
cx q[209], q[11];
cx q[207], q[12];
cx q[205], q[13];
cx q[203], q[15];
barrier q;

cx q[214], q[14];
cx q[216], q[29];
cx q[218], q[45];
cx q[220], q[63];
cx q[222], q[110];
cx q[224], q[101];
barrier q;

cx q[15], q[214];
cx q[13], q[216];
cx q[12], q[218];
cx q[11], q[220];
cx q[10], q[222];
cx q[113], q[224];
barrier q;

cx q[28], q[216];
cx q[44], q[218];
cx q[62], q[220];
cx q[109], q[222];
cx q[98], q[224];
barrier q;

cx q[9], q[216];
cx q[8], q[218];
cx q[7], q[220];
cx q[6], q[222];
cx q[5], q[224];
barrier q;

cx q[214], q[14];
cx q[216], q[29];
cx q[218], q[45];
cx q[220], q[63];
cx q[222], q[110];
cx q[224], q[101];
barrier q;

cx q[235], q[102];
cx q[233], q[0];
cx q[231], q[1];
cx q[229], q[2];
cx q[227], q[3];
cx q[225], q[4];
barrier q;

cx q[101], q[235];
cx q[110], q[233];
cx q[63], q[231];
cx q[45], q[229];
cx q[29], q[227];
cx q[14], q[225];
barrier q;

cx q[5], q[233];
cx q[6], q[231];
cx q[7], q[229];
cx q[8], q[227];
cx q[9], q[225];
barrier q;

cx q[111], q[233];
cx q[64], q[231];
cx q[46], q[229];
cx q[30], q[227];
cx q[16], q[225];
barrier q;

cx q[235], q[102];
cx q[233], q[0];
cx q[231], q[1];
cx q[229], q[2];
cx q[227], q[3];
cx q[225], q[4];
barrier q;

