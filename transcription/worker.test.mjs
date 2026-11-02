import test from 'node:test';
import assert from 'node:assert/strict';
import {selectWords,audible} from './worker.mjs';
test('overlap context selects each core once and ignores absent timing',()=>{
  const chunks=[{text:'one',timestamp:[4,5]},{text:'two',timestamp:[6,7]},{text:'missing',timestamp:[8,null]}];
  assert.deepEqual(selectWords(chunks,15,20,40,50),[{start:21,end:22,text:'two'}]);
});
test('silence is skipped',()=>{
  assert.equal(Boolean(audible(new Float32Array(16000))),false);
  assert.equal(Boolean(audible(new Float32Array(16000).fill(.1))),true);
});
