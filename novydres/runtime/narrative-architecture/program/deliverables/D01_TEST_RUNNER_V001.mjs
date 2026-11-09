// Initial D01 fixtures. Run: node D01_TEST_RUNNER_V001.mjs D01_TEST_VECTORS_V001.json
import {readFileSync} from 'node:fs';
import {runFixtureSuite} from './D01_VALIDATOR_V001.mjs';
const file=process.argv[2]||'D01_TEST_VECTORS_V001.json';
const cases=JSON.parse(readFileSync(file,'utf8'));
const results=runFixtureSuite(cases);
console.log(JSON.stringify({suite:cases.suite_id,passed:results.filter(x=>x.result==='PASS').length,total:results.length,results},null,2));
if(results.some(x=>x.result!=='PASS'))process.exitCode=1;
