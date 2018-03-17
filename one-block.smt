(declare-const A1 Int)
(declare-const A2 Int)

(assert (>= A1 0))
(assert (<= A1 115))
(assert (>= A2 0))
(assert (<= A2 115))

(check-sat)
(get-model)
