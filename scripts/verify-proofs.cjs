// Verify saved finalized receipts, source commitments and every credit transition.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=name=>JSON.parse(fs.readFileSync(path.join(root,'proofs',name+'.json'),'utf8'));
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const canonical=v=>JSON.stringify(v,(_,x)=>x&&!Array.isArray(x)&&typeof x==='object'?Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b))):x);
const same=(a,b)=>assert.equal(canonical(a),canonical(b));
const m=read('deployment');
assert.equal(m.network,'studionet');assert.equal(m.chain_id,61999);assert.equal(m.exact_source_match,true);
assert.equal(m.source_sha256,hash(fs.readFileSync(path.join(root,'contracts/work_fair.py'))));
const record=JSON.parse(fs.readFileSync(path.join(root,'records/intake.json')));
assert.equal(m.sources.intake.sha256,hash(fs.readFileSync(path.join(root,'records/intake.json'))));
assert.equal(m.sources.intake.url,`https://raw.githubusercontent.com/gabrieladash123-bit/work-fair/${m.fixture_revision}/records/intake.json`);
assert.equal(m.transactions.length,7);
for(const tx of m.transactions){
  const r=read(tx.label+'-receipt');
  assert.equal(r.statusName||r.status_name,'FINALIZED');assert.equal(r.result_name,'MAJORITY_AGREE');
  assert.ok(['SUCCESS','FINISHED_WITH_RETURN'].includes(r.txExecutionResultName||r.consensus_data?.leader_receipt?.[0]?.execution_result));
  assert.equal((r.hash||r.transactionHash||r.transaction_hash).toLowerCase(),tx.hash.toLowerCase());
  assert.ok(Object.values(r.consensus_data.votes).filter(v=>v==='agree').length>=3);
  if(tx.action!=='deploy')assert.equal(r.to_address.toLowerCase(),m.contract_address.toLowerCase());
}
const intake=read('intake');
assert.equal(intake.contract_address,m.contract_address);
assert.equal(intake.source_sha256,m.source_sha256);
assert.equal(intake.transaction.hash,m.transactions[1].hash);
assert.equal(intake.state.source_repository,'gabrieladash123-bit/work-fair');
assert.ok(read('intake-receipt').data.calldata.readable.includes(m.sources.intake.url));
assert.ok(read('intake-receipt').data.calldata.readable.includes(m.sources.intake.sha256));
same(intake.state.batches[0].record,record);
same(intake.state.batches[0].report.jobs.map(j=>j.class),['CROSSCHECK','LOOKUP','TRANSFORM','LOOKUP','LOOKUP','BLOCKED','UNKNOWN']);
assert.equal(intake.state.batches[0].url,m.sources.intake.url);
assert.equal(intake.state.batches[0].sha256,m.sources.intake.sha256);
const tariff={LOOKUP:1,TRANSFORM:2,CROSSCHECK:4,BLOCKED:0,UNKNOWN:0};
const tenants=['amber','cobalt','jade'],weights={amber:1,cobalt:2,jade:1};
let pending={amber:[],cobalt:[],jade:[]},credit={amber:0,cobalt:0,jade:0},cursor=0;
record.jobs.forEach((job,i)=>{const c=intake.state.batches[0].report.jobs[i];assert.ok(job.specification.includes(c.quote));if(tariff[c.class])pending[job.tenant].push({id:job.id,tenant:job.tenant,cost:tariff[c.class],batch:0,class:c.class});});
same(intake.state.queues,pending);same(intake.state.deficits,credit);same(intake.state.rounds,[]);
const expected=[['cobalt-convert','jade-copy'],['cobalt-copy'],[],['amber-audit'],['amber-copy']];
let admitted=[];
for(let index=0;index<5;index++){
  const proof=read('round'+(index+1)),state=proof.state,r=state.rounds.at(-1);
  assert.equal(proof.transaction.hash,m.transactions[index+2].hash);
  assert.equal(proof.contract_address,m.contract_address);same(state.batches,intake.state.batches);
  assert.equal(proof.source_sha256,m.source_sha256);same(state.seen,intake.state.seen);
  if(index) same(state.rounds.slice(0,-1),read('round'+index).state.rounds);
  assert.equal(state.rounds.length,index+1);assert.equal(r.number,index+1);
  let left=8,issued=[];
  for(let visit=0;visit<3;visit++){
    const t=tenants[(cursor+visit)%3],v=r.visits[visit],q=pending[t];
    assert.equal(v.tenant,t);assert.equal(v.before,credit[t]);
    const grant=q.length?weights[t]:0,clipped=q.length?Math.max(0,credit[t]+grant-8):0;
    assert.equal(v.grant,grant);assert.equal(v.clipped,clipped);
    credit[t]=q.length?Math.min(8,credit[t]+grant):0;
    let spent=0;
    while(q.length && q[0].cost<=credit[t] && q[0].cost<=left){const j=q.shift();credit[t]-=j.cost;left-=j.cost;spent+=j.cost;issued.push(j);}
    assert.equal(v.spent,spent);assert.equal(v.discarded,q.length?0:credit[t]);
    if(!q.length)credit[t]=0;
    assert.equal(v.after,credit[t]);assert.equal(v.before+v.grant,v.clipped+v.spent+v.discarded+v.after);
  }
  cursor=(cursor+1)%3;
  same(r.admitted,issued);same(issued.map(j=>j.id),expected[index]);same(state.queues,pending);same(state.deficits,credit);
  assert.equal(state.cursor,cursor);assert.equal(r.spent,8-left);
  admitted.push(...issued);
}
assert.equal(admitted.length,5);assert.equal(new Set(admitted.map(j=>j.id)).size,5);
assert.ok(Object.values(pending).every(q=>q.length===0));
console.log('Verified 7 finalized receipts, exact source hash, exclusions, FIFO admissions and 15 conserved credit visits.');
