(module
  (memory $mem 1)
  (export "memory" (memory $mem))
  (func $add (param $a i32) (param $b i32) (result i32)
    (return 
      (i32.add
        (local.get $a)
        (local.get $b)
      )
    )
  )
  (export "add" (func $add))
  (func $sub (param $a i32) (param $b i32) (result i32)
    (return 
      (i32.sub
        (local.get $a)
        (local.get $b)
      )
    )
  )
  (export "sub" (func $sub))
  (func $mul (param $a i32) (param $b i32) (result i32)
    (return 
      (i32.mul
        (local.get $a)
        (local.get $b)
      )
    )
  )
  (export "mul" (func $mul))
  (func $div (param $a i32) (param $b i32) (result i32)
    (return 
      (i32.div_s
        (local.get $a)
        (local.get $b)
      )
    )
  )
  (export "div" (func $div))
  (func $mod (param $a i32) (param $b i32) (result i32)
    (return 
      (i32.rem_s
        (local.get $a)
        (local.get $b)
      )
    )
  )
  (export "mod" (func $mod))
)