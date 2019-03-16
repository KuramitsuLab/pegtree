assume n: Int

fizzbuzz(n) =
    | "FizzBuzz" if n % 15 == 0
    | "Fizz"     if n % 3 == 0
    | "Buzz"     if n % 5 == 0
    | n          otherwise
