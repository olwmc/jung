# Jung

Jung is a small lisp-like calculator language I wrote for my final project for CSC402 at URI. 

Jung compiles down to a bytecode which is read by a VM. The VM and bytecode are heavily modeled after Dr. Lutz Hamel's Exp1Bytecode.

I used this project as a first endeavor to compilers. I learned an incredible amount about the code generation process and the nature of compilation.

## Running Jung
```bash
python main.py examples/fizzbuzz.lisp
```

## Examples
### Iterative and Recursive Factorial
```lisp
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
```