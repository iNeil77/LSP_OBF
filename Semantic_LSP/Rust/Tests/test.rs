use rand::distributions::WeightedIndex;
use rand::prelude::*;
use std::cell::RefCell;
use std::cmp::{min, Ordering};
use std::collections::BinaryHeap;
use std::rc::Rc;

type NodeRef = Rc<RefCell<Node>>;
type HypothesisRef = Rc<RefCell<Hypothesis>>;
type Agenda = BinaryHeap<Hypothesis>;

struct Hypothesis {
    node_ref: NodeRef,
    next: Option<HypothesisRef>,
    fx: f64,
    gx: f64,
}