(set-logic LIA)

(synth-fun f ((x Int) (y Int)) Int
   ((Start Int (x
                y
                0 1 -1 2 -2
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
(declare-var a Int)
(declare-var b Int)

(constraint (=> (= x y) (= 0 (f x y))))
(constraint (=> (> x y) (= (f x y) 1)))
(constraint (=> (< a b) (= (f a b) -1)))
(check-synth)

