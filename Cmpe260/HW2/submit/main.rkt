; muhammet ali topcu
; 2020400147
; compiling: yes
; complete: yes
#lang racket

(provide (all-defined-out))

; read and parse the input file
(define parse (lambda (input-file)
        (letrec (
            [input-port (open-input-file input-file)]
            [read-and-combine (lambda ()
                (let ([line (read input-port)])
                    (if (eof-object? line)
                        '()
                        (append `(,line) (read-and-combine))
                    )
                )
            )]
            )
            (read-and-combine)
        )
    )
)
(define create-hash (lambda (vars values)
        (letrec (
            [create-hash-iter (lambda (vars values hash)
                (if (null? vars)
                    hash
                    (create-hash-iter (cdr vars) (cdr values) (hash-set hash (car vars) (car values)))
                )
            )]
            )
            (create-hash-iter vars values (hash))
        )
    )
)

(define add-to-hash (lambda (old-hash new-hash)
        (foldl (lambda (key hash) (hash-set hash key (hash-ref new-hash key)))
            old-hash
            (hash-keys new-hash)
        )
    )
)

(define eval-program (lambda (program-str)
        (get (eval-exprs (parse program-str) empty-state) '-r)
    )
)



; You can use higher-order functions apply, map, foldl, foldr. You are also encouraged to
; use anonymous functions with the help of lambda.

;(define-namespace-anchor anc)
;(define ns (namespace-anchor->namespace anc))
; bu 2li eval calıssın diye lazımmış, eval sonuna da ns koymak lazımmış anlamadım neden?
; bunları eval-expr ile evaluate edip en son statementte -r'a bakıcaz, true ise then-exprs, false ise else-exprs giricez, sonra.



; 2.1 empty-state
(define empty-state (hash))



; 2.2 (get state var). if var is undefined in state, then don't eval it.
(define (get state var)
    (cond
        ((hash-has-key? state var) (hash-ref state var))
        (else (eval var))
    )
)


; 2.3 (put state var val)
(define (put state var val) (hash-set state var val))



; 2.4 (:= var val-expr state).
(define (:= var val-expr state)
    ;(put (eval-expr val-expr state) var (get (eval-expr val-expr state) '-r))
    (let ([new-state (eval-expr val-expr state)])
        (put new-state var (get new-state '-r)))
)


; 2.5 (if: test-expr then-exprs else-exprs state)
(define (if: test-expr then-exprs else-exprs state)
    (let ([test-result (eval-expr test-expr state)])
        (cond
            ((eq? (get test-result '-r) #t) (eval-exprs then-exprs test-result))
            (else (eval-exprs else-exprs test-result))
        )
    )
    ;(cond
        ;((eq? (get (eval-expr test-expr state) '-r) #t) (eval-exprs then-exprs (eval-expr test-expr state)))
        ;(else (eval-exprs else-exprs (eval-expr test-expr state)))
    ;)
)



; 2.6 (while: test-expr body-exprs state)

(define (while: test-expr body-exprs state)
    (let ([test-result (eval-expr test-expr state)])
        (cond
            ((eq? (get test-result '-r) #t) (while: test-expr body-exprs (eval-exprs body-exprs test-result)))
            (else (eval-expr test-expr state))
        )
    )
    ;(cond
        ;((eq? (get (eval-expr test-expr state) '-r) #t) (while: test-expr body-exprs (eval-exprs body-exprs (eval-expr test-expr state))))
        ;;(else (put state '-r (eval-expr body-exprs (eval-expr test-expr state))))
        ;(else (eval-expr test-expr state))
    ;)
)

(define (eval-args args state)
    ; takes list of args and evals each of them and returns the list
    (cond
        ((null? args) '())
        (else (cons (get (eval-expr (car args) state) '-r) (eval-args (cdr args) state)))
    )
)

; 2.7 (func params body-exprs state)

(define (func params body-exprs state)
    (put state '-r (lambda args (get (eval-exprs body-exprs (put-list state (map cons params (eval-args args state)))) '-r)))
)
;(drop-right (map-eval (list params) state) 1) params yerine?
; (get (eval-expr args state) '-r)

; suggested, completed

;(map-eval lst state) ;
(define (map-eval lst state)
    (cond
        ((null? lst) (list state))
        (else 
            (let ([first-result (eval-expr (car lst) state)])
                (cons (get first-result '-r) (map-eval (cdr lst) first-result))
            )
            
        ;(cons (get (eval-expr (car lst) state) '-r) (map-eval (cdr lst) (eval-expr (car lst) state)))
        )
    )
)


; a util function for func to put a list of key-value pairs to a hash
(define (put-list state lst)
    (cond
        ((null? lst) state)
        (else (put-list (put state (car (car lst)) (cdr (car lst))) (cdr lst)))
    )
)





; 2.8 (eval-expr expr state)
; eval-expr should evaluate the expr and put the result in the state's '-r key and return the state.

(define (eval-expr expr state)
    (cond
        ((list? expr) 
          (cond 
            ((eq? (car expr) ':=) (apply (eval (car expr)) (cdr (append expr (list state))) ))
            ((eq? (car expr) 'if:) (apply (eval (car expr)) (cdr (append expr (list state))) ))
            ((eq? (car expr) 'while:) (apply (eval (car expr)) (cdr (append expr (list state))) ))
            ((eq? (car expr) 'func) (apply (eval (car expr)) (cdr (append expr (list state))) ))
            ((eq? (car expr) 'lambda) (put state '-r (eval expr)))
            ((procedure? (eval (get state (car expr)))) (put state '-r (apply (eval (get state (car expr))) (drop-right (map-eval (cdr expr) state) 1))))
            
            ;((eq? (car expr) 'printf) (put state '-r (apply (eval (car expr)) (cdr expr)) ))
            (else (put state '-r (drop-right (map-eval expr state) 1) ))

            ;((procedure? (eval (car expr) ns)) (map-eval (cdr expr) state)) ; alttaki böyle de olabiliyor
            ;((symbol? (car expr)) (put state '-r (apply (eval (car expr) ns) (drop-right (map-eval (cdr expr) state) 1))))
          )
        )
        ((eq? expr #t) (put state '-r #t))
        ((eq? expr #f) (put state '-r #f))
        ((hash-has-key? state expr) (put state '-r (hash-ref state expr)))
        ((string? expr) (put state '-r (eval expr)))
        ;((symbol? expr) 
            ;(cond 
                ;((procedure? (eval expr)) (put state '-r (eval expr)))
                ;(else (put state '-r expr))
            ;)
        ;)
        ((number? expr) (put state '-r expr))
    )
)

; 2.9 (eval-exprs exprs state)
(define (eval-exprs exprs state)
    (cond
        ((null? exprs) state)
        (else (eval-exprs (cdr exprs) (eval-expr (car exprs) state)))
    )
)






#|
"EX2.1"
; Examples for 2.1
empty-state

"EX2.2"
; Examples for 2.2
(get (hash 'a 5) 'a)
(get (hash 'a 5) '+)
(get (hash 'a 5) '3)
(get (hash 'a 5) ''a) ; bunu nasıl check edicez?
;(get (hash 'a 5) 'b) ; b undefined hata veriyor, sıkıntı değil galiba ***

"EX2.3"
; Examples for 2.3
(put (hash 'a 5) 'a 6)
(put (hash 'a 5) 'b 6)


"EX2.4"
; Examples for 2.4
(:= 'a 5 (hash 'b 6))
(:= 'a '(+ 2 3) (hash 'b 6))
(:= 'a 'b (hash 'b 6))
(:= 'a '(+ 2 b) (hash 'b 6))
(:= 'b '(* b b) (hash 'b 6))
(:= 'a '+ (hash 'b 6))
((get (:= 'square '(lambda (x) (* x x)) (hash 'b 6)) 'square) 5)
;((get (:= 'my-func '(func (x) ((:= x (* 5 x)) (:= y (+ x x)))) (hash 'b 6)) 'my-func) 5)   ; func sıkıntılı ***

"EX2.5"
; Examples for 2.5
(if: '#t '(1) '(2) empty-state)
(if: '#f '(1) '(2) empty-state)
(if: '#t '(a) '(b) (hash 'a 5 'b 6))
(if: '#f '(a) '((:= a (* a b))) (hash 'a 5 'b 6))
(if: '(> a b) '((:= a (* a b))) '((:= b (* a b))) (hash 'a 5 'b 6))


"EX2.6"
; Examples for 2.6
(while: '(> a 0) '((:= a (- a 1))) (hash 'a 5))
(while: '(< a 10) '((printf "a=~a\n" a) (:= a (+ a 1))) (hash 'a 0)) ; bu sıkıntılı ***


"EX2.7" ; func da sıkıntılı !!!
(func '(x y) '((:= x (* x x)) (:= y (- y x))) empty-state)
((get (func '(x y) '((:= x (* x x)) (:= y (- y x))) empty-state) '-r) 5 10)
((get (func '(x) '((:= x (* x x)) (:= y (- y x))) (hash 'y 100)) '-r) 5)


"EX-map-eval"
; map-eval examples
(map-eval '((+ 1 2) (* 3 4)) empty-state)
(map-eval '(a b c d) (hash 'a 1 'b 2 'c 3 'd 4))


"EX2.8"
; Examples for 2.8
(eval-expr '5 empty-state)
(eval-expr 'a (hash 'a 5))
(eval-expr '(+ 1 2) empty-state)
(eval-expr '(+ a b) (hash 'a 1 'b 2))
(eval-expr '(:= a 5) empty-state)
(eval-expr '(:= a (+ 1 2)) empty-state)
(eval-expr '(if: (< 1 2) (5) (10)) empty-state)
(eval-expr '(if: (< 2 1) (5) (10)) empty-state)
(eval-expr '(while: (< a 10) ((:= a (+ a 1)))) (hash 'a 0))
;(eval-expr '(func (x y) (+ x y)) empty-state)
|#

