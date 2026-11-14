//! Fate-native QA readout (owner architecture).
//!
//! P1 (exposure only, no behaviour change): every QA row carries the
//! Fate grasp record — which blocks (fragments) the question stimulus
//! activated, their Fate scores, the full candidate score series
//! (s1..sk, descending) produced by the field readout, and the grasped
//! corpus line. Downstream (gateway, tests) must read this record
//! instead of reconstructing grasp from answer text or lexical tracks.
//!
//! The gate reading over `candidate_scores` is intentionally NOT
//! decided here yet: recorded series are the offline test vectors for
//! calibrating a Fate-equation gate (check_convergence over the diff
//! series) before any algebra is replaced.

use serde::{Deserialize, Serialize};

/// Fate grasp record for one question.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct FateGrasp {
    /// Activated block (fragment) ids, best first.
    pub selected_fragments: Vec<String>,
    /// Fate score per selected block, aligned with `selected_fragments`.
    pub fragment_scores: Vec<f64>,
    /// Candidate line score series, descending (s1 >= s2 >= ...).
    pub candidate_scores: Vec<f64>,
    /// Corpus index of the grasped line, when the field produced one.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub grasped_idx: Option<usize>,
}

impl FateGrasp {
    pub fn build(
        selected_fragments: Vec<String>,
        fragment_scores: Vec<f64>,
        candidate_scores: Vec<f64>,
        grasped_idx: Option<usize>,
    ) -> Option<Self> {
        if selected_fragments.is_empty() && candidate_scores.is_empty() {
            return None;
        }
        Some(Self {
            selected_fragments,
            fragment_scores,
            candidate_scores,
            grasped_idx,
        })
    }

    /// Adjacent differences of the candidate series: [s1-s2, s2-s3, ...].
    /// This is the series a Fate convergence judgement would read.
    pub fn diff_series(&self) -> Vec<f64> {
        self.candidate_scores
            .windows(2)
            .map(|w| w[0] - w[1])
            .collect()
    }

    /// Top-two margin (s1 - s2), 0 when fewer than two candidates.
    pub fn margin(&self) -> f64 {
        if self.candidate_scores.len() >= 2 {
            self.candidate_scores[0] - self.candidate_scores[1]
        } else {
            0.0
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Recorded offline vectors (valhalla-server probes, 2026-11-14):
    // multimodal q1: grasp correct, gate abstains on a near-tie series.
    #[test]
    fn recorded_q1_near_tie_series() {
        let g = FateGrasp::build(
            vec!["seg_1".into(), "seg_2".into()],
            vec![0.31, 0.29],
            vec![1.3665087882942228, 1.3662427025488026],
            Some(0),
        )
        .unwrap();
        assert_eq!(g.grasped_idx, Some(0));
        assert!((g.margin() - 0.0002660857454202).abs() < 1e-12);
        assert_eq!(g.diff_series().len(), 1);
    }

    #[test]
    fn empty_grasp_is_none() {
        assert!(FateGrasp::build(vec![], vec![], vec![], None).is_none());
    }
}
