(print "Running Factorials...")
(defun rfact [n]
    (cond 
        ( (<= n 0) (return 1) )
        ( True     (return (* n (rfact (- n 1)))))))

(defun ifact [n]
    (store product 1)
    (for [j] 1 n
        (store product (* product j))
    )
    (return product)
)

(print "Recursive 5!: " (rfact 5))
(print "Iterative 5!: " (ifact 5))