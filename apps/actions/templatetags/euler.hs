
-- 1

prb1 = sum $ filter (\x -> mod x 3==0 || mod x 5==0) [1..999]


-- 2

fib' :: (Ord a, Num a) => a -> a -> a -> [a]
fib' a b mx = if b < mx then a : fib' b (a+b) mx else [a]

prb2 = sum $ filter even (fib' 1 2 4000000)


-- 3





-- 4



-- 5


-- 6


-- 7

isPrime :: (Eq a, Integral a, Enum a, Num a) => a -> Bool
isPrime x = not $ any divisible $ takeWhile notTooBig [2..] where
     divisible y = x `mod`y == 0
     notTooBig y = y*y <= x

primes' = filter isPrime [1..]

-- 8



