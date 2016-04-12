(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cdr (cdr s)))
)

(define (square x) (* x x))

(define (pow b n)
  (cond
      ((= n 0) '1)
      ((= (remainder n 2) 0) (* (pow b (/ n 2)) (pow b (/ n 2))))
      (else (* b (pow b (- n 1))))
  )
)

(define (ordered? s)
(cond
  ((null? s) #t)
  ((null? (cdr s)) #t)
  ((> (car s) (cadr s)) #f)
  (else (ordered? (cdr s)))
)
)

(define (no-repeats s)
  (define (filter f lst)
    (cond ((null? lst) '())
          ((f (car lst)) (cons (car lst) (filter f (cdr lst))))
          (else (filter f (cdr lst))))
  )
  (if (null? s)
  s
  (cons (car s) (no-repeats (filter (lambda (x) (not (= (car s) x))) (cdr s))))
)
)

(define (nodots s)
  (define (dotted? s)
      (and (pair? s) (not (or (pair? (cdr s)) (null? (cdr s))))))
  (cond
    ((null? s) s)
    ((dotted? s) (list (nodots (car s)) (cdr s)))
    ((pair? s) (cons (nodots (car s)) (nodots (cdr s))))
    (else s)
  )
)

; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond ((empty? s) false)
          ((> (car s) v) #f)
          ((= (car s) v) #t)
          (else (contains? (cdr s) v)) ; replace this line
          ))

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return len(s) == 0
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)
(define (add s v)
    (cond ((empty? s) (list v))
          ((contains? s v) s)
          ((> (car s) v) (cons v s))
          (else (cons (car s) (add (cdr s) v))) ; replace this line
          ))

(define (intersect s t)
    (cond ((or (empty? s) (empty? t)) nil)
          ((= (car s) (car t)) (cons (car s) (intersect (cdr s) (cdr t))))
          ((< (car s) (car t)) (intersect (cdr s) t))
          (else (> (car s) (car t)) (intersect s (cdr t))) ; replace this line
          ))

; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
    (cond ((empty? s) t)
          ((empty? t) s)
          ((= (car s) (car t)) (cons (car s) (union (cdr s) (cdr t))))
          ((> (car s) (car t)) (cons (car t) (union s (cdr t))))
          (else (< (car s) (car t)) (cons (car s) (union (cdr s) t))) ; replace this line
          ))

; A data abstraction for binary trees where nil represents the empty tree
(define (tree label left right) (list label left right))
(define (label t) (car t))
(define (left t) (cadr t))
(define (right t) (caddr t))
(define (empty? s) (null? s))
(define (leaf label) (tree label nil nil))
(define (in? t v)
    (cond ((empty? t) false)
          ((= (label t) v) #t)
          ((< (label t) v) (in? (right t) v))
          (else (> (label t) v) (in? (left t) v))
          ))

; Equivalent Python code, for your reference:
;
; def contains(s, v):
;     if s.is_empty:
;         return False
;     elif s.label == v:
;         return True
;     elif s.label < v:
;         return contains(s.right, v)
;     elif s.label > v:
;         return contains(s.left, v)
(define (as-list t)
    (define (as-list+ t s)
       (if (empty? t) s
       (as-list+ (left t) (cons (label t) (as-list+ (right t) s)))
    )
    )
  (as-list+ t nil)
  )
