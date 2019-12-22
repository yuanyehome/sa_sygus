(set-logic LIA)
(synth-fun findIdx ( (y1 Int) (y2 Int) (k1 Int)) Int ((Start Int ( 0 1 2 y1 y2 k1 (ite BoolExpr Start Start))) (BoolExpr Bool ((< Start Start) (<= Start Start) (> Start Start) (>= Start Start)))))
(declare-var k Int)
(declare-var m Int)
(declare-var x1 Int)
(declare-var x2 Int)
(declare-var x3 Int)
(declare-var a1 Int)
(declare-var a2 Int)
(declare-var a3 Int)
(constraint (=> (< x1 x2) (=> (< k x1) (= (findIdx x1 x2 k) 0))))
(constraint (=> (< x1 x2) (=> (> m x2) (= (findIdx x1 x2 m) 2))))
(constraint (=> (< x1 x2) (=> (and (> k x1) (< k x2)) (= (findIdx x1 x2 k) 1))))
(constraint (=> (> a1 a2) (=> (> k a1) (= (findIdx a1 a2 k) 2))))
(constraint (=> (> a1 a2) (=> (< m a2) (= (findIdx a1 a2 m) 0))))
(constraint (=> (> a1 a2) (=> (and (> k a2) (< k a1)) (= (findIdx a1 a2 k) 1))))
(constraint (=> (= a1 a2) (= (findIdx a1 a2 k) -1)))
(check-synth)