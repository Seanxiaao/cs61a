;; Extra Scheme Questions ;;

; Q8
(define (max a b) (if (> a b) a b))
(define (min a b) (if (> a b) b a))
(define (gcd a b)
  (if (= b 0)
        a
        (gcd b (remainder a b))
        )
)

;;; Tests
(gcd 24 60)
; expect 12
(gcd 1071 462)
; expect 21

; Q9
(define (split-at lst n)

)
