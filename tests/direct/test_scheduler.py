import ast
import hashlib
import itertools
import json
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
REPO = 'gabrieladash123-bit/work-fair'
BODY = (ROOT/'records/intake.json').read_bytes()
URL = f"https://raw.githubusercontent.com/{REPO}/{'a'*40}/records/intake.json"
SHA = hashlib.sha256(BODY).hexdigest()
CLASSES = ['CROSSCHECK','LOOKUP','TRANSFORM','LOOKUP','LOOKUP','BLOCKED','UNKNOWN']

def report():
    return {'jobs':[{'id':row['id'],'class':kind,'quote':row['specification']} for row,kind in zip(json.loads(BODY)['jobs'],CLASSES)]}

def mock(vm, leader=None, own=None, anchors=None, body=BODY):
    vm.clear_mocks()
    vm.mock_web(re.escape(URL),{'status':200,'body':body})
    vm.mock_llm(r'.*WORKFAIR-LEADER.*',json.dumps(report() if leader is None else leader))
    vm.mock_llm(r'.*WORKFAIR-VALIDATOR.*',json.dumps(report() if own is None else own))
    vm.mock_llm(r'.*WORKFAIR-ANCHORS.*',json.dumps({'valid':[True]*7 if anchors is None else anchors}))

@pytest.fixture
def fair(direct_deploy):
    return direct_deploy(str(ROOT/'contracts/work_fair.py'),REPO)

def enqueue(c,vm):
    mock(vm)
    c.enqueue(URL,SHA)

def test_weighted_admission_and_expensive_head_eventually_served(fair,direct_vm):
    enqueue(fair,direct_vm)
    expected=[['cobalt-convert','jade-copy'],['cobalt-copy'],[],['amber-audit'],['amber-copy']]
    for ids in expected:
        fair.advance()
        state=fair.get_state()
        assert [j['id'] for j in state['rounds'][-1]['admitted']]==ids
    assert not any(state['queues'].values())
    assert state['deficits']=={'amber':0,'cobalt':0,'jade':0}
    assert state['seen']==[row['id'] for row in json.loads(BODY)['jobs']]

def test_blocked_and_unknown_never_enter_queue(fair,direct_vm):
    enqueue(fair,direct_vm)
    assert [j['id'] for j in fair.get_state()['queues']['jade']]==['jade-copy']
    assert len(fair.get_state()['batches'][0]['report']['jobs'])==7

def test_validator_independent_agreement(fair,direct_vm):
    enqueue(fair,direct_vm)
    assert direct_vm.run_validator() is True

@pytest.mark.parametrize('index,kind',[(0,'LOOKUP'),(5,'CROSSCHECK'),(6,'TRANSFORM')])
def test_validator_rejects_cost_and_readiness_disagreement(fair,direct_vm,index,kind):
    enqueue(fair,direct_vm)
    own=report();own['jobs'][index]['class']=kind
    mock(direct_vm,own=own)
    assert direct_vm.run_validator() is False

def test_validator_checks_exclusion_quote(fair,direct_vm):
    enqueue(fair,direct_vm)
    mock(direct_vm,anchors=[True]*6+[False])
    assert direct_vm.run_validator() is False

def test_validator_refetches_bytes(fair,direct_vm):
    enqueue(fair,direct_vm)
    mock(direct_vm,body=BODY+b' ')
    assert direct_vm.run_validator() is False

@pytest.mark.parametrize('kind',['omit','unknown-enum','foreign-quote','reorder'])
def test_invalid_classification_reverts(fair,direct_vm,kind):
    bad=report()
    if kind=='omit':bad['jobs'].pop()
    if kind=='unknown-enum':bad['jobs'][0]['class']='CHEAP'
    if kind=='foreign-quote':bad['jobs'][0]['quote']=bad['jobs'][1]['quote']
    if kind=='reorder':bad['jobs'].reverse()
    mock(direct_vm,leader=bad)
    with direct_vm.expect_revert():fair.enqueue(URL,SHA)
    assert fair.get_state()['batches']==[]

def test_duplicate_source_reverts(fair,direct_vm):
    enqueue(fair,direct_vm)
    with direct_vm.expect_revert('Duplicate source'):fair.enqueue(URL,SHA)

def test_unpinned_source_reverts(fair,direct_vm):
    with direct_vm.expect_revert('pinned publisher'):fair.enqueue(URL.replace('a'*40,'main'),SHA)

def test_source_hash_reverts(fair,direct_vm):
    mock(direct_vm,body=BODY+b' ')
    with direct_vm.expect_revert('commitment mismatch'):fair.enqueue(URL,SHA)

def test_empty_round_reverts(fair,direct_vm):
    with direct_vm.expect_revert('Empty scheduler'):fair.advance()

def pure_scheduler():
    tree=ast.parse((ROOT/'contracts/work_fair.py').read_text())
    wanted=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('canon','schedule')]
    ns={'json':json,'TENANTS':('amber','cobalt','jade'),'WEIGHTS':(1,2,1)}
    exec(compile(ast.Module(body=wanted,type_ignores=[]),'scheduler','exec'),ns)
    return ns['schedule']

def test_exhaustive_fifo_budget_and_credit_conservation():
    schedule=pure_scheduler()
    for costs in itertools.product((1,2,4),repeat=6):
        queues={t:[{'id':f'{t}-{i}','cost':costs[k*2+i]} for i in range(2)] for k,t in enumerate(('amber','cobalt','jade'))}
        original=json.loads(json.dumps(queues))
        s={'queues':queues,'deficits':{t:0 for t in queues},'cursor':0,'rounds':[]}
        seen=[]
        for _ in range(16):
            if not any(s['queues'].values()):break
            previous=json.dumps(s,sort_keys=True)
            nxt=schedule(s)
            assert json.dumps(s,sort_keys=True)==previous
            r=nxt['rounds'][-1]
            assert r['spent']==sum(j['cost'] for j in r['admitted'])<=8
            for v in r['visits']:
                assert v['before']+v['grant']==v['clipped']+v['spent']+v['discarded']+v['after']
            seen.extend(r['admitted']);s=nxt
        assert not any(s['queues'].values())
        assert len(seen)==6 and len({j['id'] for j in seen})==6
        for tenant in queues:assert [j for j in seen if j['id'].startswith(tenant)]==original[tenant]

def test_empty_tenant_cannot_bank_credit():
    s={'queues':{'amber':[{'id':'expensive','cost':4}],'cobalt':[],'jade':[]},'deficits':{'amber':0,'cobalt':0,'jade':0},'cursor':0,'rounds':[]}
    for _ in range(3):s=pure_scheduler()(s)
    assert s['deficits']=={'amber':3,'cobalt':0,'jade':0}
    assert all(not r['admitted'] for r in s['rounds'])

def test_global_budget_does_not_bypass_head_and_clipping_is_accounted():
    s={'queues':{'amber':[{'id':'a','cost':4}],'cobalt':[{'id':'c1','cost':4},{'id':'c2','cost':4}],'jade':[{'id':'j','cost':1}]},'deficits':{'amber':3,'cobalt':7,'jade':0},'cursor':0,'rounds':[]}
    result=pure_scheduler()(s)
    r=result['rounds'][0]
    assert [j['id'] for j in r['admitted']]==['a','c1']
    assert r['spent']==8 and r['visits'][1]['clipped']==1
    assert result['queues']['cobalt']==[{'id':'c2','cost':4}]
    assert result['deficits']=={'amber':0,'cobalt':4,'jade':1}

def test_different_source_cannot_reuse_job_ids(fair,direct_vm):
    enqueue(fair,direct_vm)
    body=BODY+b'\n'
    mock(direct_vm,body=body)
    with direct_vm.expect_revert('Duplicate job'):fair.enqueue(URL,hashlib.sha256(body).hexdigest())
    assert len(fair.get_state()['batches'])==1
