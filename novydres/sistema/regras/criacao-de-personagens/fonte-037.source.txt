import copy
import json
import random
import unittest
from webfirst_core import (create_store, append_event, apply_pool_roll, apply_rouse,
                           score_pool, validate_store, parse_store, serialize_store,
                           plan_drive_replace, ValidationError)

class WebfirstTests(unittest.TestCase):
    def setUp(self):
        self.s=create_store()
    def do(self,kind="PLAYER_DECLARATION", actor="pc",text="Tento convencer o segurança.",**kwargs):
        cmd={"kind":kind,"actor":actor,"text":text,**kwargs}
        if kind=="PLAYER_DECLARATION":
            cmd.setdefault("declaration",text)
            cmd.setdefault("declaration_ref","CHAT-USER-001")
            cmd.setdefault("declaration_class","ATTEMPT")
        self.s=append_event(self.s,cmd)
        return self.s
    def prep(self,pool=5,hunger=2,difficulty=3):
        self.do(kind='SYSTEM',actor='system',text='ROLL_PREP',
                causal_refs=['EVT-000001'],rule_ref='V5_BASIC_POOL',
                source={'roll_spec':{'pool':pool,'hunger':hunger,'difficulty':difficulty,'rule_ref':'V5_BASIC_POOL'}})
        return self.s['events'][-1]['id']
    def test_T01_attempt_does_not_move_pc(self):
        self.do()
        self.assertEqual(self.s['state'],{})
        with self.assertRaises(ValidationError):
            self.do(kind='PLAYER_DECLARATION',text='Tento convencer o segurança.',deltas=[{"field":"pc.location","before":None,"after":"interior","reason":"assumption"}])
    def test_T02_hypothetical_not_attack(self):
        with self.assertRaises(ValidationError):
            self.do(kind='NPC_ACTION',actor='pc',text='Ataquei o guarda')
        self.assertEqual(self.s['events'],[])
    def test_T03_plan_not_fact(self):
        with self.assertRaises(ValidationError):
            self.do(kind='GM_PLAN',actor='gm',text='Um NPC pensa em assassinar outro',deltas=[{'field':'npc.x.alive','before':None,'after':False,'reason':'plan'}])
    def test_T04_optional_spend_requires_approval(self):
        self.do()
        with self.assertRaises(ValidationError):
            self.do(kind='WORLD_EVENT',actor='world',text='WP gasto',causal_refs=['EVT-000001'],rule_ref='V5_BASIC_POOL',deltas=[{"field":"pc.willpower.current","before":None,"after":2,"reason":"spent"}])
    def test_T05_roll_requires_committed_source_and_dice_are_raw(self):
        with self.assertRaises(ValidationError):apply_pool_roll(self.s,{"pool":5,"hunger":2,"difficulty":3,"rule_ref":"V5_BASIC_POOL"},source_event_id='EVT-000001')
        self.do()
        src=self.prep()
        outcome=apply_pool_roll(self.s,{"pool":5,"hunger":2,"difficulty":3,"rule_ref":"V5_BASIC_POOL"},source_event_id=src,rng=random.Random(52))
        self.assertEqual(len(outcome['rolls'][0]['normal'])+len(outcome['rolls'][0]['hunger']),5)
        self.assertEqual(validate_store(outcome)['rolls'],1)
    def test_T06_hunger_cannot_change_silently(self):
        self.do()
        with self.assertRaises(ValidationError):
            self.do(kind='WORLD_EVENT',actor='world',text='Hunger arbitrariamente sobe',deltas=[{"field":"pc.hunger","before":None,"after":3,"reason":"nothing"}])
    def test_T07_npc_knowledge_not_invented(self):
        with self.assertRaises(ValidationError):
            self.do(kind='NPC_ACTION',actor='npc-a',text='Ele usa segredo',knowledge_used=['secret-vampire'])
    def test_T08_npc_claim_not_fact(self):
        self.do(kind='NPC_CLAIM',actor='npc-a',text='Dizem que João morreu')
        self.assertEqual(self.s['state'],{})
        self.assertEqual(self.s['events'][0]['kind'],'NPC_CLAIM')
    def test_T09_restore_from_serialised_drive_snapshot(self):
        self.do()
        s2=parse_store(serialize_store(self.s))
        self.assertEqual(s2,self.s)
        self.assertEqual(validate_store(s2)['last_event'],'EVT-000001')
    def test_T10_revision_concurrent_prefix_changes_rejected(self):
        self.do()
        base=serialize_store(self.s)
        alternative=copy.deepcopy(self.s)
        alternative['events'][0]['text']='O jogador entrou.'
        with self.assertRaises(ValidationError):plan_drive_replace(base,alternative)
    def test_T11_canon_readonly(self):
        with self.assertRaises(ValidationError):self.do(kind='WORLD_EVENT',actor='world',text='Agora há um novo raion',canon_change=True)
    def test_T12_correction_requires_approval_and_keeps_prior(self):
        self.do()
        with self.assertRaises(ValidationError):self.do(kind='CORRECTION',actor='gm',text='corrigir',target_id='EVT-000001')
        self.do(kind='CORRECTION',actor='gm',text='corrigir',target_id='EVT-000001',player_approval='CHAT-USER-002')
        self.assertEqual(len(self.s['events']),2)
        self.assertEqual(self.s['events'][0]['text'],'Tento convencer o segurança.')
    def test_tampered_chain_rejected(self):
        self.do()
        self.s['events'][0]['hash']='fake'
        with self.assertRaises(ValidationError): validate_store(self.s)
    def test_state_before_rejected(self):
        self.do(kind='WORLD_EVENT',actor='world',text='A porta abre',deltas=[{'field':'door.open','before':None,'after':True,'reason':'guard action'}])
        with self.assertRaises(ValidationError):
            self.do(kind='WORLD_EVENT',actor='world',text='A porta fecha',deltas=[{'field':'door.open','before':None,'after':False,'reason':'wrong before'}])
    def test_roll_messy_and_critical(self):
        r=score_pool([10,6,10,5],[10,1],difficulty=3)
        self.assertTrue(r['messy_critical'])
        self.assertTrue(r['passed'])
        self.assertEqual(r['critical_pairs'],1)
    def test_roll_failure_bestial(self):
        r=score_pool([2,3,4],[1],difficulty=3)
        self.assertTrue(r['bestial_failure'])
    def test_roll_tampering_detected(self):
        self.do()
        src=self.prep(pool=3,hunger=1,difficulty=2)
        s=apply_pool_roll(self.s,{"pool":3,"hunger":1,"difficulty":2},source_event_id=src,rng=random.Random(2))
        s['rolls'][0]['computed']['successes']+=1
        with self.assertRaises(ValidationError):validate_store(s)
    def test_rouse_real_d10_and_no_implicit_hunger(self):
        self.do()
        self.do(kind="SYSTEM",actor="system",text="ROUSE_PREP",causal_refs=["EVT-000001"],rule_ref="V5_BASIC_ROUSE",source={"roll_spec":{"rule_ref":"V5_BASIC_ROUSE"}})
        s=apply_rouse(self.s,source_event_id='EVT-000002',rng=random.Random(8))
        self.assertEqual(len(s['rolls']),1)
        self.assertEqual(s['state'],{})
    def test_attempt_classification_cannot_set_effect(self):
        self.do()
        with self.assertRaises(ValidationError):
            self.do(kind='PLAYER_DECLARATION',text='Entro no prédio',declaration_class='ATTEMPT',deltas=[{'field':'pc.location','before':None,'after':'inside','reason':'attempt'}])
    def test_pc_cannot_be_actor_of_world_event(self):
        with self.assertRaises(ValidationError):self.do(kind='WORLD_EVENT',actor='pc',text='PC foi embora')
    def test_versioning_event_id_sequence(self):
        self.do()
        self.do(kind='WORLD_EVENT',actor='world',text='A porta abre',causal_refs=['EVT-000001'])
        self.assertEqual(self.s['last_seq'],2)
        self.assertEqual(validate_store(self.s)['last_event'],'EVT-000002')
    def test_predeclaration_mismatch_rejected(self):
        self.do()
        src=self.prep(pool=6,hunger=2,difficulty=3)
        with self.assertRaises(ValidationError):
            apply_pool_roll(self.s,{"pool":5,"hunger":2,"difficulty":3},source_event_id=src)
    def test_same_preparation_cannot_be_rolled_twice(self):
        self.do()
        src=self.prep()
        s=apply_pool_roll(self.s,{"pool":5,"hunger":2,"difficulty":3},source_event_id=src,rng=random.Random(2))
        with self.assertRaises(ValidationError):
            apply_pool_roll(s,{"pool":5,"hunger":2,"difficulty":3},source_event_id=src)
    def test_no_user_event_in_empty_store(self):
        self.assertEqual(validate_store(self.s)['events'],0)
        self.assertEqual(self.s['chronicle_id'],None)

if __name__=='__main__': unittest.main()
