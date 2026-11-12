// ADR-001 C05 — optional diagnostic for isolated fictional examples.
// Not a narration generator, mandatory per-scene gate, or authority to apply
// successor rules; contextual literary assessment remains separate.
const fail=(code)=>{const error=new Error(code);error.code=code;throw error;};
const isNonempty=s=>typeof s==='string'&&s.trim().length>0;
export function examineFictionalFrame(frame) {
 if(frame?.test_only!==true)fail('NOT_AN_ISOLATED_FIXTURE');
 if(frame.uses_actual_campaign_event===true)fail('CAMPAIGN_SOURCE_MIXED');
 if(frame.narrator_chose_pc_action===true)fail('PLAYER_AGENCY_OVERRIDE');
 if(frame.npc?.disposition_quota_required===true)fail('NUMERIC_MOOD_QUOTA_REINTRODUCED');
 if(frame.npc?.automatic_compliance_from_courtesy===true)fail('NPC_AUTONOMY_LOST');
 if(frame.social?.won===true&&frame.social?.concession_delivered!==true)
   fail('EARNED_CONCESSION_REMOVED');
 if(frame.social?.won===true&&frame.social?.automatic_friendship===true)
   fail('SOCIAL_SUCCESS_OVERGENERALIZED');
 if(frame.pending_intention?.exists===true&&frame.pending_intention?.lost_without_cause===true)
   fail('INTENTION_DROPPED');
 if(frame.ellipsis?.substantial===true&&frame.ellipsis?.performed===true &&
    frame.ellipsis?.priorities_known!==true)fail('PRIORITIES_BEFORE_LEAP_REQUIRED');
 if(frame.ellipsis?.consumes_material_choice===true)fail('MATERIAL_CHOICE_CONSUMED_OFFSCREEN');
 if(frame.mystery?.material_clue===true&&!isNonempty(frame.mystery?.truth_pinned_ref))
   fail('MYSTERY_TRUTH_NOT_FIXED');
 if(frame.mystery?.truth_changed_to_match_clue===true)fail('MYSTERY_RETCON');
 if(frame.mechanics?.awarded_xp_without_source===true)fail('INVENTED_XP');
 if(frame.mechanics?.rerolled_after_recovery===true)fail('REROLL_ON_RECOVERY');
 if(frame.family?.harm_mandated_for_horror===true || frame.family?.invulnerable===true)
   fail('FAMILY_OUTCOME_MANDATED');
 if(frame.correction?.material===true&&frame.correction?.consent_required===true &&
    frame.correction?.consent_granted!==true)fail('MATERIAL_RETCON_UNAPPROVED');
 if(frame.output_delivered===true&&frame.transaction?.confirmed!==true)
   fail('NARRATED_WITHOUT_CONFIRMED_PERSISTENCE');
 if(frame.legacy_per_scene_manifest_required===true)fail('OLD_CADENCE_REINTRODUCED');
 return {status:'REVIEW_READY_NOT_LITERARY_CERTIFIED',classification:'TEST_ONLY',
   note:'Checks declared invariants only. Source adequacy and prose need contextual review.'};
}
// Strict separation: this is evidence mapping, NOT a prose scoring function.
// The B05 review was in a separate Web conversation, not blinded.
export function correlateFrozenBReview(exercises,followup,review) {
 if(!Array.isArray(exercises)||exercises.length!==8)fail('FROZEN_EXERCISES_MISSING');
 const ids=exercises.map(x=>x.id);
 if(new Set(ids).size!==8||ids.some((id,i)=>id!==('N-0'+(i+1))))fail('EXERCISE_IDS_CHANGED');
 for(const x of exercises)if(!isNonempty(x.response)||!isNonempty(x.setup))
   fail('FROZEN_EXERCISE_CONTENT_MISSING');
 if(followup?.id!=='N-06-RESULT'||!isNonempty(followup.narrated_result))
   fail('N06_CONSEQUENCE_NOT_REVIEWABLE');
 const assessments=review?.narrative;
 if(!Array.isArray(assessments)||assessments.length!==8)fail('CONTEXTUAL_REVIEW_NOT_FOUND');
 for(const entry of assessments) {
   if(!ids.includes(entry.id)||!isNonempty(entry.basis))fail('REVIEW_EVIDENCE_MISSING');
   if(entry.id==='N-06' && entry.result!=='INITIAL_INSUFFICIENT_FOLLOWUP_PASS_CONTEXTUAL')
     fail('N06_HISTORICAL_FAILURE_ERASED');
 }
 if(!review.limitations?.some(x=>x.includes('blind')))fail('REVIEW_NOT_BLIND_LIMIT_MISSING');
 return {status:'HISTORICAL_CONTEXTUAL_REVIEW_REUSED',case_count:8,followup:'N-06-RESULT',
  independent_conversation:true,blind_review:false,runtime_certified:false};
}
