(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))

; Some utility functions that you may find useful to implement.
(define (map proc items)
(if (null? items)
         '()
         (cons (proc (car items)) (map proc (cdr items)))))


(define (cons-all first rests)
(if (null? rests)
    'nil
    (cons (cons first (car rests)) (cons-all first (cdr rests))))
)

(define (zip pairs)
(define firsts (map (lambda (pair) (car pair)) pairs))
(define seconds (map (lambda (pair) (cadr pair)) pairs))
(list firsts seconds)
  )

(define (min lst)
    (cond ((null? (cdr lst)) (car lst))
          ((< (car lst) (min (cdr lst))) (car lst))
          (else (min (cdr lst))))
)

;; Problem 18
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN Question 18
  (define (enumerate_helper n s)
    (if (eq? nil s)
        s
        (cons (list n (car s)) (enumerate_helper (+ n 1) (cdr s)))
        )
  )
  (enumerate_helper 0 s)
  )
  ; END Question 18

;; Problem 19
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN Question 19
  (cond ((= total 0) (car denoms))
        ((or (< total 0) (null? denoms)) nil)
        (else (cons (cons-all (car denoms) (list-change total
                     (cdr denoms)))
                 (cons-all (car denoms) (list-change (- total
                        (car denoms))
                     denoms )))))
)
  ; END Question 19

;; Problem 20
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr)
         ; BEGIN Question 20
         expr
         ; END Question 20
         )
        ((quoted? expr)
         ; BEGIN Question 20
         expr
         ; END Question 20
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
           (append (list form params) (map analyze body))
           ; END Question 20
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
           (define zipped (zip values))
           (define parameters (car zipped))
           (define param_values (map analyze (cadr zipped)))
           (define fn (append (list 'lambda parameters) (map analyze body)))
           (cons fn param_values)

           ; END Question 20
           ))
        (else
         ; BEGIN Question 20
         (map analyze expr)
         ; END Question 20
         )))

;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
(define (hax d k)
  ; BEGIN Question 21
  'REPLACE-THIS-LINE
  )
  ; END Question 21
