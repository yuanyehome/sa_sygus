; max3.sl
; Synthesize the maximum of 2 integers, from a purely declarative spec

(set-logic LIA)

(synth-fun max2 ((xx Int) (yy Int)) Int
    ((Start Int (xx
                 yy
                 0
                 1
                 (+ Start Start)
                 (- Start Start)
                 (ite StartBool Start Start)))
     (StartBool Bool ((and StartBool StartBool)
                      (or  StartBool StartBool)
                      (not StartBool)
                      (<=  Start Start)
                      (=   Start Start)
                      (>=  Start Start)))))

(declare-var x Int)
(declare-var y Int)

(constraint (>= (max2 y x) (+ y 1)))
(constraint (<= (+ y 1) (max2 x y)))
(constraint (or (= (+ x 1) (max2 x y))
				(= (+ y 1) (max2 x y))))


(check-synth)

