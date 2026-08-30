# Handoff — INT 02h IVT-write quiescent re-verification (run session)

Date: 2026-08-30
Scope: run the quiescent-write disproof probe against the 2026-08-25
int02_vector_write_ub decision; record results. No verdict promotion.

## 1. Verified this session

- BIOS NMI_PTR is a WORD label at ABS0:0008; all four BIOS writes target
  only the offset word (C7 06 0008): 04D3=0F78 POST, 06B6=F815 RAM-test,
  06DC=0F78 reset. Segment word 000A is never written by the BIOS.
  (manual-verified, bios_grep 68/1344/1631/1649; facts nmi_ptr_bios_word_only)
- READONLY probe (pure BASIC DEF SEG 0 + PEEK; no machine code needed) on
  a fresh boot reads 0000:0008=3960 (0F78), 0000:000A=61440 (F000).
  Stock INT 02h vector at BASIC runtime = F000:0F78.
  (empirical; facts stock_nmi_vector_empirical)
- Same-boot probe (BASIC pre-read + IVTWR asm + BASIC post-read) on a
  fresh boot: pre = wr-readback = post = 3960:61440, RETURNED OK,
  keyboard fine. Clean run; falsifier not observed. Verdict per contract
  ivt_write_quiescent_sameboot: failed_to_disprove.
- The earlier IVTWR run (same DATA, non-fresh boot) read 0000:0000 with
  keyboard fine — recorded as conflict; leading explanation is session
  residue, untested. (facts ivt_zero_vector_session_residue)
- facts.md has no nmi_chain_detail heading; Rule 7 and the project doc
  point to it. Pointer drift. (facts nmi_chain_detail_pointer_drift)

## 2. Open questions

- Does the stock vector hold F000:0F78 on every boot path, or only on a
  fresh cold boot?
- What wrote 0000:0000 in the earlier session? Residue hypothesis untested.
- Is one failed_to_disprove sufficient to reopen the custom INT 02h
  handler line? Not decided here.

## 3. Loose ends

- int02_vector_write_ub (2026-08-25) stands unmodified. One survival does
  not supersede an empirical decision.
- The earlier 0000:0000 run's pre-state was not recorded — process gap.
- nmi_chain_detail heading missing; needs a facts.md entry or a Rule 7
  pointer fix.

## 4. Suggested next scope

Repeat the same-boot probe on a second fresh boot. If it fails to
disprove again, propose a supersedes path for int02_vector_write_ub and
decide on reopening the custom INT 02h handler. Alternatively, root-cause
the 0000:0000 session-residue observation first.

## 5. Ground truth

- docs/anchors/IRPING2.ASM / IRPING2.BAS — transport regression
- docs/anchors/CH0CAL.ASM / CH0CAL.bas — functional primary regression
- No new anchors this session: IVTWR is a disproof probe; failed_to_disprove
  does not earn anchor status.
