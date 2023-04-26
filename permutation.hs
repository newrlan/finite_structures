data Cycle = Cycle [Int] deriving (Show)

apply_ :: Int -> [Int] -> Int -> Int
apply_ h [x] k
    | x == k = h
    | otherwise = k
apply_ h (x:y:arr) k
    | x == k = y
    | otherwise = apply_ h (y:arr) k

apply [_] k = k
apply (x:arr) k = apply_ x (x:arr) k

mull :: [[Int]] -> Int -> Int
mull arr k = foldl (flip $ apply) k arr

del_elem y [] = []
del_elem y (x:xs)
    | y == x = xs
    | otherwise = x: del_elem y xs

pop_elem y xs = y: del_elem y xs


cicles_ f [] = ys
cicles_ f (x:xs) = x: cicles f (y:ys)
    where
        y = f x
        ys = del_elem y xs
    
