// NOVYDRES D01 lightweight semantic validator V001.
// PROPOSED_NON_OPERATIONAL, no hidden lore; full JSON Schema engine belongs to D10.
const TERMINAL = new Set(["RESOLVED","FAILED","ABANDONED_WITH_CONSEQUENCES","RESOLVED_OFFSCREEN_WITH_EVIDENCE","SUPERSEDED_WITH_PROVENANCE"]);
const nonEmpty = value => typeof value==="string" && value.trim().length>0;
const list = value => Array.isArray(value);
export function validateD01(kind, doc) {
 const errors=[]; const fail=(condition,code)=>{if(condition)errors.push(code)};
 if(!doc||typeof doc!=="object"||Array.isArray(doc))return ["INVALID_RECORD"];
 const idKeys={chronicle:"chronicle_id",marco:"marco_id",history_episode:"history_episode_id",plot:"plot_id",story:"story_id",scene:"scene_id",beat:"beat_id",thread:"thread_id",actor:"actor_id",relationship:"edge_id",clue:"clue_id",clock:"clock_id",knowledge:"knowledge_id",ledger:"ledger_id",retcon:"change_id"};
 if(!idKeys[kind])return ["UNKNOWN_KIND"];
 fail(!nonEmpty(doc[idKeys[kind]]),"ID_REQUIRED");
 if(kind==="plot"){
   fail(!nonEmpty(doc.independent_pressure),"INDEPENDENT_PRESSURE_REQUIRED");
   fail(!nonEmpty(doc.pc_hook_noncoercive),"NONCOERCIVE_HOOK_REQUIRED");
   fail(!nonEmpty(doc.closure_test),"CLOSURE_TEST_REQUIRED");
   fail(!list(doc.outcomes)||!["SUCCESS","FAILURE","REFUSAL","OFFSCREEN"].every(route=>doc.outcomes.some(x=>x.route===route)),"OUTCOME_ROUTE_COVERAGE");
   fail(doc.status==="SUSPENDED"&&(!doc.suspension||!nonEmpty(doc.suspension.reason)||!nonEmpty(doc.suspension.review_owner)||!nonEmpty(doc.suspension.review_trigger)),"SUSPENSION_REVIEW_REQUIRED");
   fail(TERMINAL.has(doc.status)&&(!list(doc.terminal_evidence_refs)||doc.terminal_evidence_refs.length===0),"TERMINAL_EVIDENCE_REQUIRED");
   if(list(doc.plot_links))for(const edge of doc.plot_links)fail(edge.kind==="CAUSAL"&&(!list(edge.sources)||!edge.sources.some(s=>s.verification==="VERIFIED")),"CAUSAL_LINK_EVIDENCE_REQUIRED");
 }
 if(kind==="story"){
   fail(!nonEmpty(doc.nonmandatory_entry),"ENTRY_NONCOERCIVE_REQUIRED");
   fail(!nonEmpty(doc.refusal_path),"STORY_REFUSAL_REQUIRED");
   fail(!nonEmpty(doc.failure_path),"STORY_FAILURE_REQUIRED");
   fail(!list(doc.closure_routes)||doc.closure_routes.length===0,"STORY_LOCAL_CLOSURE_REQUIRED");
 }
 if(kind==="scene"){
   fail(!nonEmpty(doc.potential_change),"SCENE_POTENTIAL_CHANGE_REQUIRED");
   fail(!nonEmpty(doc.refusal_path),"SCENE_REFUSAL_REQUIRED");
   fail(!nonEmpty(doc.pre_roll_gate),"SCENE_PREROLL_REQUIRED");
 }
 if(kind==="beat")fail(!nonEmpty(doc.trigger)||!nonEmpty(doc.if_not_triggered),"BEAT_CONDITION_REQUIRED");
 if(kind==="scene"||kind==="beat")fail(doc.forces_pc_action===true,"PLAYER_AGENCY_VIOLATION");
 if(kind==="clue"){
   if(doc.critical===true){
     fail(!list(doc.discovery_routes)||new Set(doc.discovery_routes.map(x=>x.independent_mechanism)).size<2,"CRITICAL_CLUE_ROUTES");
     fail(doc.truth_lock_status!=="LOCKED","AUTHORIAL_TRUTH_NOT_LOCKED");
     fail(doc.truth_lock_status==="LOCKED"&&!nonEmpty(doc.truth_lock_ref),"TRUTH_REF_REQUIRED");
   }
 }
 if(kind==="clock"){
   fail(!nonEmpty(doc.actor_id)||!nonEmpty(doc.tick_trigger),"CLOCK_CAUSAL_TRIGGER_REQUIRED");
   fail(!Number.isInteger(doc.current)||!Number.isInteger(doc.maximum)||doc.maximum<1||doc.current<0||doc.current>doc.maximum,"CLOCK_RANGE_INVALID");
 }
 if(kind==="actor")fail(!nonEmpty(doc.as_of_event_id)||!list(doc.knowledge_refs),"ACTOR_EPISTEMIC_CHECKPOINT_REQUIRED");
 if(kind==="knowledge")fail(!nonEmpty(doc.knower_id)||!nonEmpty(doc.acquisition_ref)||!nonEmpty(doc.as_of_event_id),"KNOWLEDGE_ACQUISITION_REQUIRED");
 if(kind==="relationship")fail(!nonEmpty(doc.from_id)||!nonEmpty(doc.to_id)||doc.from_id===doc.to_id,"RELATIONSHIP_DIRECTION_REQUIRED");
 if(kind==="marco")fail(!nonEmpty(doc.functional_goal)||!nonEmpty(doc.coverage_test)||!nonEmpty(doc.coherence_test)||!nonEmpty(doc.consequence_test),"D1_SUFFICIENCY_REQUIRED");
 if(kind==="history_episode")fail(!list(doc.material_output_refs)||doc.material_output_refs.length===0,"D1_MATERIAL_OUTPUT_REQUIRED");
 if(kind==="retcon"){
   fail(["RETCON_SOFT","RETCON_HARD"].includes(doc.kind)&&doc.approval_required!==true,"RETCON_APPROVAL_REQUIRED");
   fail(["RETCON_SOFT","RETCON_HARD"].includes(doc.kind)&&doc.status==="APPLIED_VERSIONED"&&!nonEmpty(doc.approval_decision_id),"RETCON_APPROVAL_EVIDENCE_REQUIRED");
 }
 return [...new Set(errors)];
}
export function validatePhaseHandoff(h){
 const errors=[];
 if(h?.spoiler_class!=="PLAYER_SAFE")errors.push("HANDOFF_NOT_PLAYER_SAFE");
 if(!nonEmpty(h?.phase)||!nonEmpty(h?.repository)||!nonEmpty(h?.design_branch))errors.push("HANDOFF_IDENTITY_REQUIRED");
 if(h?.phase==="D12"&&h?.next_phase==="NARRADOR"&&!(h?.cycle?.status==="READY_FOR_NARRATOR"&&h?.cycle?.next_role==="NARRADOR"&&h?.player_authorization?.verified===true&&h?.readback_pass===true))errors.push("NARRATOR_GATE_NOT_MET");
 return errors;
}
export function runFixtureSuite(suite){
 if(!suite||!Array.isArray(suite.cases))throw new Error("INVALID_FIXTURE_SUITE");
 return suite.cases.map(c=>{
   const errors=c.kind==="handoff"?validatePhaseHandoff(c.record):validateD01(c.kind,c.record);
   const pass=c.expected==="PASS"?errors.length===0:errors.includes(c.expected_error);
   return {id:c.id,result:pass?"PASS":"FAIL",errors};
 });
}
