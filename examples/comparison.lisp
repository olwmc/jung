(print "Running Epley/Brzycki comparison")
# https://en.wikipedia.org/wiki/One-repetition_maximum#Epley_formula
(defun epley [weight reps]
    (return (* weight (+ 1 (/ reps 30))) )
)

# https://en.wikipedia.org/wiki/One-repetition_maximum#Brzycki
(defun brzycki [weight reps]
    (return
        (/ weight (- 1.0278 (* reps 0.0278)))
    )
)

(print (epley 300 3))
(print (brzycki 300 3))