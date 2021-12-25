(defun fizzbuzz [n]
    (for [x] 1 n
        (cond
            ( (and (not (% x 3)) (not (% x 5) )) 
                (print "Fizzbuzz") )
                
            ( (= (% x 3) 0) (print "Fizz") )
            
            ( (= (% x 5) 0) (print "Buzz") )
            
            ( True    (print x) ))))

(fizzbuzz 15)