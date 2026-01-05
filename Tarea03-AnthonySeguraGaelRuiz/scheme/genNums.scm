#lang scheme

(define genNums
  (lambda (n puerto)
  (cond ((> n 0)
     (display (+ (random 20) 1) puerto) (newline puerto) (genNums (- n 1) puerto)))))

(call-with-output-file "scheme.txt"
  (lambda (puerto)
    (genNums 1000000 puerto))
  #:exists 'replace)